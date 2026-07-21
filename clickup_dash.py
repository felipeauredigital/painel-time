# -*- coding: utf-8 -*-
"""
Painel de acompanhamento do time (E-SCALE & FENIX) a partir do ClickUp.

Puxa TODAS as tarefas (abertas + concluídas) dos membros, calcula:
  - tarefas em atraso (por pessoa),
  - comportamento/histórico completo (conclusões, % no prazo, check em lote, criadas),
  - tarefas mal cadastradas (sem responsável / sem prazo) com provável dono via
    campos personalizados Account / Gestor de Tráfego / Squad.
Gera model.json e, em seguida, o dashboard.html (via render.py).

Uso:
  1) Gere um token pessoal em ClickUp > Settings > Apps > API Token (começa com "pk_").
  2) Informe o token de uma destas formas (o script tenta nesta ordem):
       - variável de ambiente:  set CLICKUP_TOKEN=pk_xxx   (Windows)  /  export CLICKUP_TOKEN=pk_xxx
       - arquivo .clickup_token nesta pasta (uma linha com o token)  [gitignored]
  3) Rode:  python clickup_dash.py
     Opções:  --no-fetch  (reaproveita data/*.json já baixado, só recalcula e regera o HTML)
              --render-only (só regenera o HTML a partir do model.json)
"""
import os, sys, json, time, datetime, re, urllib.request, urllib.parse, urllib.error

# Console do Windows costuma ser cp1252; garante UTF-8 na saída.
try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
os.makedirs(DATA, exist_ok=True)

API = "https://api.clickup.com/api/v2"
TEAM_ID = "36963360"

# ---- Membros dos times (uid do ClickUp) ----
MEMBERS = {
    81464977:  ("Lucas Caldeira",  "E-SCALE", "Head"),
    55085676:  ("Carlos Barbosa",  "E-SCALE", "Account"),
    54912242:  ("Ray Junio",       "E-SCALE", "Gestor de Tráfego"),
    87447111:  ("Izabela Galdino", "E-SCALE", "Account"),
    87413647:  ("Rafael Alves",    "E-SCALE", "Gestor de Tráfego"),
    81465000:  ("Felipe M. Assunção", "E-SCALE", "Account"),
    206579907: ("Thiago Zagnoli",  "FENIX",   "Head"),
    87318381:  ("Vinicius Andrade","FENIX",   "Account"),
    60944498:  ("Vitor Dumont",    "FENIX",   "Gestor de Tráfego"),
    96672993:  ("Rafael Ramos",    "FENIX",   "Account"),
    87448889:  ("Kaio Felipe",     "FENIX",   "Gestor de Tráfego"),
    118026171: ("Patrick Lima",    "FENIX",   "Account"),
    87445783:  ("Carlos Nobre",    "FENIX",   "Gestor de Tráfego"),
    96624276:  ("Tiago Lamêu",     "FENIX",   "Gestor de Tráfego"),
}
MEMBER_ORDER = list(MEMBERS.keys())

# ---- Listas ----
EXCLUDE_LISTS = {"Campanhas de Tráfego"}          # legada, o time não usa mais
NAO_ACAO_LISTS = {"Otimização de Campanhas"}      # anúncios rodando/pausados: não é "pendência de ação"

# As listas a varrer são DESCOBERTAS automaticamente nestes espaços (assim novas listas
# entram sozinhas). Hoje: Operacional (onde vive o trabalho diário dos times).
SCAN_SPACES = ["90113535859"]                     # Operacional
EXTRA_LISTS = {"901109318541": "Processos de Artes"}   # lista relevante fora da Operacional
# Não baixar (legada / registros automáticos, não são tarefas):
FETCH_EXCLUDE = {"Campanhas de Tráfego", "NPS Respostas recebidas"}
# "Sem prazo" só é erro em listas de entregável datado (evita marcar card de cliente /
# reunião recorrente / template de kickoff, que normalmente não têm prazo).
DUE_EXPECTED_LISTS = {"Processos de Artes", "Planejamento e Gestão de CRM", "Otimização de Campanhas"}
# "Mal cadastradas" só faz sentido nas listas de trabalho de cliente (evita floodar com
# briefings / etapas de processo, que são de topo e sem responsável por natureza).
MALFORMED_LISTS = {"Gestão de Projetos", "Processos de Artes", "Planejamento e Gestão de CRM",
                   "Otimização de Campanhas", "Envio de NPS", "Kickoff", "Entrada do cliente",
                   "Agenda de clientes", "Coleta de indicações"}

# ---- Campos personalizados (descobertos na lista Gestão de Projetos) ----
CF_ACCOUNT = "89b1f5f2-cbd4-4f83-a26e-35237a3979b9"
CF_GESTOR  = "109e26b9-be03-4c1c-bfe6-8ce55f893d4d"
CF_SQUAD   = "41162abd-5add-4ba8-8021-8e429437f907"
SQUAD_OPTION_TEAM = {  # option_id -> time (squad) — usado p/ vincular a tarefa ao time
    "3ccda512-5eb3-42a8-ae50-df68130b8323": "ADFORCE",
    "9da4d887-eeea-4861-8e2a-c121e942375b": "G.O.A.T",
    "57826e7f-16f9-46c1-b8d1-ecf9b6d767e3": "BULLS",
    "e7381c3d-7fa2-49dc-b751-3119a12480b6": "E-SCALE",
    "7a77de2a-1dda-40fc-a6ff-154df5251ccf": "COMERCIAL",
    "5b22d724-ccb2-4d9f-a4d9-f722e60387c5": "FENIX",
    "9616694f-428d-4b66-aca3-ff11f29fe815": "BACKOFFICE",
    # VALHALLA (0f534b85-...) fica de fora do painel (mesmo critério do churn)
}

# ---- Controle de churn: lista "Gestão de empresas" e seus campos ----
EMPRESAS_LIST = "223068147"
CF_FEE     = "be8d6d21-be62-4605-a6ce-341464979dd3"   # currency BRL
CF_ENTRADA = "f4e17a53-690b-41e6-b1ff-43af524c6a70"   # date
CF_AVISO   = "d9a5449b-43c5-4c73-9637-db41a3b76da3"   # date
CF_SAIDA   = "6baa81c3-bd42-4d9e-974a-2fde4d015bfd"   # date
# Squad é o MESMO campo (CF_SQUAD). O valor vem como orderindex (int) do dropdown:
SQUAD_ORDER = {0: "ADFORCE", 1: "G.O.A.T", 2: "BULLS", 3: "VALHALLA",
               4: "E-SCALE", 5: "COMERCIAL", 6: "FENIX", 7: "BACKOFFICE"}
# Squads fora do painel INTEIRO (churn E tarefas): totais, squads, pessoas, clientes e times.
# COMERCIAL e BACKOFFICE são de outros setores; VALHALLA foi descontinuado.
EXCLUDE_SQUADS = {"VALHALLA", "COMERCIAL", "BACKOFFICE"}
SQUAD_ALL = ["ADFORCE", "G.O.A.T", "BULLS", "E-SCALE", "FENIX"]
# Situação do cliente (status da tarefa) → grupo de churn:
ST_ATIVO   = {"ativo", "inadimplente", "pendência adm"}          # carteira ativa (base)
ST_ONBOARD = {"processo de entrada", "aguardando inicio"}        # entrando (ainda não na base)
ST_AVISO   = {"aviso"}                                           # em aviso (risco de churn)
ST_CHURN   = {"rescisão", "finalizado"}                          # saíram
ST_PAUSA   = {"projeto pausado"}                                 # pausado

TZ = datetime.timezone(datetime.timedelta(hours=-3))  # Brasília

# ------------------------------------------------------------------ token
def get_token():
    tok = os.environ.get("CLICKUP_TOKEN", "").strip()
    if tok:
        return tok
    for fn in ("token.txt", ".clickup_token"):
        p = os.path.join(HERE, fn)
        if os.path.exists(p):
            t = open(p, encoding="utf-8-sig").read().strip()
            if t and "cole" not in t.lower():   # ignora o placeholder
                return t
    sys.exit(
        "\n>>> Falta o token do ClickUp <<<\n"
        "1) Abra o arquivo 'token.txt' (nesta pasta) no Bloco de Notas.\n"
        "2) Apague o texto que estiver lá e cole o seu token (começa com 'pk_').\n"
        "3) Salve e rode de novo (ou dê duplo-clique em 'gerar-painel.bat').\n"
        "Gere o token em: ClickUp > Settings > Apps > API Token.\n")

# ------------------------------------------------------------------ http
class ApiError(Exception):
    pass

def api_get(path, params=None, token=None):
    qs = ""
    if params:
        qs = "?" + urllib.parse.urlencode(params, doseq=True)
    url = API + path + qs
    for attempt in range(6):
        req = urllib.request.Request(url, headers={"Authorization": token, "Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                return json.loads(r.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            if e.code == 429:  # rate limit
                wait = int(e.headers.get("Retry-After", "8"))
                print(f"  rate limit; aguardando {wait}s...")
                time.sleep(wait + 1); continue
            body = e.read().decode("utf-8", "ignore")
            raise ApiError(f"API {e.code} em {url}: {body}")
        except urllib.error.URLError as e:
            print(f"  rede instável ({e}); tentativa {attempt+1}..."); time.sleep(3); continue
    raise ApiError("Falha ao chamar a API após várias tentativas.")

def paginate(path, base_params, token, label=""):
    """Percorre todas as páginas (100/tarefas por página)."""
    out, page = [], 0
    while True:
        p = dict(base_params); p["page"] = page
        data = api_get(path, p, token)
        tasks = data.get("tasks", [])
        out.extend(tasks)
        print(f"  {label} página {page}: +{len(tasks)} (total {len(out)})")
        if data.get("last_page") is True or len(tasks) < 100:
            break
        page += 1
        if page > 300:
            print("  (limite de segurança de 300 páginas atingido)"); break
        time.sleep(0.7)  # respeita rate limit (~85 req/min, abaixo do teto de 100)
    return out

# ------------------------------------------------------------------ fetch
def fetch_all(token):
    scan_lists = discover_lists(token, SCAN_SPACES)
    print(f"Listas descobertas para varrer: {len(scan_lists)}")
    print("Baixando tarefas das listas do time (abertas + concluídas)...")
    tasks, seen = [], set()
    for lid, lname in scan_lists.items():
        try:
            rows = paginate(f"/list/{lid}/task",
                            {"include_closed": "true", "subtasks": "true"}, token, f"lista {lname}")
            for t in rows:
                if t["id"] not in seen:
                    seen.add(t["id"]); tasks.append(t)
        except ApiError as e:
            print(f"  [aviso] pulando lista '{lname}' (sem acesso ou erro): {str(e)[:80]}")
    json.dump(tasks, open(os.path.join(DATA, "tasks.json"), "w", encoding="utf-8"), ensure_ascii=False)
    json.dump(fetch_avatars(token), open(os.path.join(DATA, "avatars.json"), "w", encoding="utf-8"), ensure_ascii=False)
    fetch_empresas(token)
    return tasks

def fetch_empresas(token):
    """Baixa a lista 'Gestão de empresas' (fee, status, squad, account/gestor, datas de churn)."""
    print("Baixando empresas (Gestão de empresas)...")
    try:
        rows = paginate(f"/list/{EMPRESAS_LIST}/task",
                        {"include_closed": "true", "subtasks": "false"}, token, "empresas")
    except ApiError as e:
        print(f"  [aviso] não consegui baixar empresas: {str(e)[:80]}")
        rows = []
    json.dump(rows, open(os.path.join(DATA, "empresas.json"), "w", encoding="utf-8"), ensure_ascii=False)
    return rows

def discover_lists(token, space_ids):
    """Descobre todas as listas (em pastas e soltas) dos espaços informados + EXTRA_LISTS."""
    lists = dict(EXTRA_LISTS)
    for sid in space_ids:
        try:
            for l in api_get(f"/space/{sid}/list", token=token).get("lists", []):
                lists[l["id"]] = l["name"]
        except ApiError as e:
            print(f"  [aviso] listas soltas do espaço {sid}: {str(e)[:60]}")
        try:
            for f in api_get(f"/space/{sid}/folder", token=token).get("folders", []):
                for l in f.get("lists", []):
                    lists[l["id"]] = l["name"]
        except ApiError as e:
            print(f"  [aviso] pastas do espaço {sid}: {str(e)[:60]}")
    return {lid: n for lid, n in lists.items() if n not in FETCH_EXCLUDE}

def fetch_avatars(token):
    """uid -> URL da foto de perfil do ClickUp (públicas)."""
    try:
        data = api_get("/team", token=token)
    except ApiError:
        return {}
    av = {}
    for team in data.get("teams", []):
        if str(team.get("id")) == TEAM_ID:
            for m in team.get("members", []):
                u = m.get("user", {}) or {}
                if u.get("id") and u.get("profilePicture"):   # todos os membros (roster é dinâmico)
                    av[str(u["id"])] = u["profilePicture"]
    return av

# ------------------------------------------------------------------ helpers
def to_date(ms):
    if ms in (None, "", "null"):
        return None
    return datetime.datetime.fromtimestamp(int(ms) / 1000, TZ).date()

def is_closed(t):
    if t.get("date_closed"):
        return True
    st = (t.get("status") or {})
    return st.get("type") in ("closed", "done")

def member_ids_from_cf(task, cf_id):
    for f in task.get("custom_fields", []):
        if f.get("id") == cf_id and f.get("value"):
            v = f["value"]
            if isinstance(v, list):
                return [u.get("id") for u in v if isinstance(u, dict)]
    return []

def squad_team(task):
    for f in task.get("custom_fields", []):
        if f.get("id") == CF_SQUAD and f.get("value") not in (None, ""):
            t = SQUAD_OPTION_TEAM.get(str(f["value"]))
            return None if t in EXCLUDE_SQUADS else t
    return None

# Termos que aparecem em [COLCHETE] mas são TIPO de arte/etapa, não cliente.
ART_TAGS = {"fluxo", "banner", "criativo", "estático", "estatico", "email", "e-mail",
            "post", "story", "stories", "vídeo", "video", "carrossel", "feed", "reels"}

def project_from_cf(t):
    """Nome do cliente pelo campo personalizado 'Projeto' (list_relationship → Gestão de Projetos)."""
    for f in t.get("custom_fields", []):
        if f.get("type") == "list_relationship" and (f.get("name") or "").strip().lower() == "projeto":
            v = f.get("value")
            if isinstance(v, list) and v:
                nm = (v[0].get("name") or "").strip()
                if nm:
                    return nm
    return ""

def resolve_project(t, byid):
    """Cliente/projeto da tarefa. Ordem de confiança:
    1) campo personalizado 'Projeto' (é o vínculo real com o cliente);
    2) card raiz da hierarquia (sobe pelos pais);
    3) tag [XXX] no início do nome — ignorando termos de tipo de arte (FLUXO, BANNER...)."""
    nm = project_from_cf(t)
    if nm:
        return nm
    seen, cur = set(), t
    while cur.get("parent") and cur["parent"] in byid and cur["parent"] not in seen:
        seen.add(cur["parent"])
        cur = byid[cur["parent"]]
    if cur is not t:
        return (cur.get("name") or "").strip()
    m = re.match(r"\s*\[([^\]]+)\]", t.get("name", "") or "")
    if m:
        tag = m.group(1).strip()
        first = tag.split()[0].lower() if tag else ""
        if first not in ART_TAGS:
            return tag
    return ""

# ------------------------------------------------------------------ adiamentos de prazo
# A API do ClickUp não dá o histórico de mudança de prazo. Então guardamos um retrato dos
# prazos a cada rodada (state.json) e, comparando com o anterior, registramos todo adiamento
# (prazo empurrado pra frente) num log permanente (postpone_log.json). Acumula com o tempo.
STATE = os.path.join(DATA, "state.json")
PLOG = os.path.join(DATA, "postpone_log.json")

def _load(path, default):
    try:
        return json.load(open(path, encoding="utf-8"))
    except Exception:
        return default

def record_postponements(tasks, today, roster_ids=None):
    roster_ids = roster_ids if roster_ids is not None else set(MEMBERS)
    prev = _load(STATE, {})          # {id: {"due": "YYYY-MM-DD", ...}}
    log = _load(PLOG, [])
    logged = {(e["id"], e["at"], e["to"]) for e in log}  # evita duplicar na mesma rodada
    cur = {}
    for t in tasks:
        lst = (t.get("list") or {}).get("name") or "—"
        if lst in EXCLUDE_LISTS or is_closed(t):
            continue
        due = to_date(t.get("due_date"))
        uids = [a["id"] for a in t.get("assignees", []) if a["id"] in roster_ids]
        if not due or not uids:
            continue
        cur[t["id"]] = {"due": due.isoformat(), "name": t.get("name", ""), "list": lst, "uids": uids}
        p = prev.get(t["id"])
        if p and p.get("due") and p["due"] < due.isoformat():   # prazo empurrado pra frente
            ev = {"id": t["id"], "name": t.get("name", ""), "list": lst, "uids": uids,
                  "from": datetime.date.fromisoformat(p["due"]).strftime("%d/%m/%y"),
                  "to": due.strftime("%d/%m/%y"), "at": today.isoformat()}
            if (ev["id"], ev["at"], ev["to"]) not in logged:
                log.append(ev)
    json.dump(cur, open(STATE, "w", encoding="utf-8"), ensure_ascii=False)
    json.dump(log, open(PLOG, "w", encoding="utf-8"), ensure_ascii=False)
    return log

def aggregate_postponements():
    log = _load(PLOG, [])
    by = {}
    for e in log:
        d = by.setdefault(e["id"], {"id": e["id"], "name": e["name"], "list": e["list"],
                                    "uids": e.get("uids", []), "count": 0, "history": []})
        d["count"] += 1
        d["uids"] = e.get("uids", d["uids"])
        d["history"].append({"from": e["from"], "to": e["to"], "at": e["at"]})
    return sorted(by.values(), key=lambda x: -x["count"])

# ------------------------------------------------------------------ controle de churn
FEEHIST = os.path.join(DATA, "fee_history.json")

def _cf(t, cid):
    for f in t.get("custom_fields", []):
        if f.get("id") == cid:
            return f.get("value")
    return None

def _cf_currency(t, cid):
    v = _cf(t, cid)
    if v in (None, ""):
        return 0.0
    try:
        return float(str(v).replace(",", "."))
    except (ValueError, TypeError):
        return 0.0

def _cf_date(t, cid):
    d = to_date(_cf(t, cid))
    return d.isoformat() if d else None

def _cf_users(t, cid):
    v = _cf(t, cid)
    out = []
    if isinstance(v, list):
        for u in v:
            if isinstance(u, dict) and u.get("id"):
                out.append({"uid": u["id"], "name": (u.get("username") or "").strip(),
                            "avatar": u.get("profilePicture")})
    return out

def _cf_squad(t):
    for f in t.get("custom_fields", []):
        if f.get("id") == CF_SQUAD and f.get("value") not in (None, ""):
            v = f["value"]
            opts = (f.get("type_config") or {}).get("options") or []
            if isinstance(v, int) or (isinstance(v, str) and v.isdigit()):
                iv = int(v)
                for o in opts:
                    if o.get("orderindex") == iv:
                        return o.get("name")
                return SQUAD_ORDER.get(iv)
            for o in opts:
                if o.get("id") == v:
                    return o.get("name")
    return None

def is_company(t):
    """Empresa de verdade (não uma tarefa administrativa da lista): topo, com fee/entrada/squad."""
    if t.get("parent"):
        return False
    st = (t.get("status") or {}).get("status", "").lower()
    if st == "para fazer":
        return False
    return bool(_cf_currency(t, CF_FEE) > 0 or _cf_date(t, CF_ENTRADA) or _cf_squad(t))

def build_churn(empresas, variavel=None, reducoes=None, reducoes_list=None):
    """Monta o modelo de churn: fee ativo x em aviso, por squad e por pessoa (Account/Gestor).
    churn% = (fee em aviso + reduções lançadas) / (fee ativo + fee em aviso) — % do faturamento em risco.
    variavel: {"mes":..,"bySquad":{squad:{"variavel":R$}}} p/ a base Fee+Variável.
    reducoes: {squad: R$} de reduções/descontos lançados no mês (entram no churn como valor em risco)."""
    clients, people = [], {}
    sq = {}

    def squad_bucket(s):
        return sq.setdefault(s, {"squad": s, "feeAtivo": 0.0, "feeAviso": 0.0, "feeChurn": 0.0,
                                 "nAtivo": 0, "nAviso": 0, "nChurn": 0, "nOnboard": 0})

    def person(u, role, squad):
        p = people.setdefault(u["uid"], {"uid": u["uid"], "name": u["name"], "avatar": u.get("avatar"),
                                         "roles": set(), "squads": set(),
                                         "feeAtivo": 0.0, "feeAviso": 0.0, "feeChurn": 0.0,
                                         "accFee": 0.0, "gesFee": 0.0,  # fee ativo como Account / como Gestor (p/ split 65/35 do bônus)
                                         "nAtivo": 0, "nAviso": 0, "nChurn": 0})
        if role:
            p["roles"].add(role)
        if squad and squad != "—":
            p["squads"].add(squad)
        if u.get("avatar") and not p.get("avatar"):
            p["avatar"] = u["avatar"]
        return p

    for t in empresas:
        if not is_company(t):
            continue
        st = (t.get("status") or {}).get("status", "").lower()
        fee = _cf_currency(t, CF_FEE)
        squad = _cf_squad(t) or "—"
        if squad in EXCLUDE_SQUADS:      # squad fora da análise de churn (ex.: VALHALLA)
            continue
        acc = _cf_users(t, CF_ACCOUNT)
        ges = _cf_users(t, CF_GESTOR)
        grp = ("ativo" if st in ST_ATIVO else "aviso" if st in ST_AVISO
               else "churn" if st in ST_CHURN else "onboard" if st in ST_ONBOARD
               else "pausa" if st in ST_PAUSA else "outro")
        saida = _cf_date(t, CF_SAIDA)
        aviso = _cf_date(t, CF_AVISO)
        clients.append({"id": t["id"], "name": (t.get("name") or "").strip(), "fee": round(fee, 2),
                        "status": st, "grp": grp, "squad": squad,
                        "account": acc[0]["name"] if acc else None, "accountUid": acc[0]["uid"] if acc else None,
                        "gestor": ges[0]["name"] if ges else None, "gestorUid": ges[0]["uid"] if ges else None,
                        "accountUids": [u["uid"] for u in acc], "gestorUids": [u["uid"] for u in ges],
                        "entrada": _cf_date(t, CF_ENTRADA), "aviso": aviso, "saida": saida,
                        "churnDate": saida or aviso})
        S = squad_bucket(squad)
        involved = [(u, "Account") for u in acc] + [(u, "Gestor de Tráfego") for u in ges]
        if grp == "ativo":
            S["feeAtivo"] += fee; S["nAtivo"] += 1
            for u, r in involved:
                p = person(u, r, squad); p["feeAtivo"] += fee; p["nAtivo"] += 1
                if r == "Account":
                    p["accFee"] += fee
                else:
                    p["gesFee"] += fee
        elif grp == "aviso":
            S["feeAviso"] += fee; S["nAviso"] += 1
            for u, r in involved:
                p = person(u, r, squad); p["feeAviso"] += fee; p["nAviso"] += 1
        elif grp == "churn":
            S["feeChurn"] += fee; S["nChurn"] += 1
            for u, r in involved:
                p = person(u, r, squad); p["feeChurn"] += fee; p["nChurn"] += 1
        elif grp == "onboard":
            S["nOnboard"] += 1

    def churn_pct(atv, avi):
        base = atv + avi
        return round(avi / base * 100, 2) if base > 0 else 0.0

    squads = []
    for s in SQUAD_ALL + [k for k in sq if k not in SQUAD_ALL]:
        S = sq.get(s)
        if not S or (S["nAtivo"] + S["nAviso"] + S["nChurn"] == 0):
            continue
        S["churnPct"] = churn_pct(S["feeAtivo"], S["feeAviso"])
        for k in ("feeAtivo", "feeAviso", "feeChurn"):
            S[k] = round(S[k], 2)
        squads.append(S)

    ppl = []
    for p in people.values():
        if p["nAtivo"] + p["nAviso"] + p["nChurn"] == 0:
            continue
        p["roles"] = sorted(p["roles"]); p["squads"] = sorted(p["squads"])
        p["churnPct"] = churn_pct(p["feeAtivo"], p["feeAviso"])
        for k in ("feeAtivo", "feeAviso", "feeChurn", "accFee", "gesFee"):
            p[k] = round(p[k], 2)
        ppl.append(p)
    ppl.sort(key=lambda x: -(x["feeAtivo"] + x["feeAviso"]))

    # ---- Fee + Variável (comissão do mês) e Reduções lançadas (desconto/tirou serviço) ----
    vbys = (variavel or {}).get("bySquad", {})
    red_by = reducoes or {}
    for S in squads:
        v = float((vbys.get(S["squad"]) or {}).get("variavel") or 0.0)
        r = float(red_by.get(S["squad"]) or 0.0)
        S["variavel"] = round(v, 2)
        S["reducao"] = round(r, 2)
        S["feeAtivoVar"] = round(S["feeAtivo"] + v, 2)
        S["churnPct"] = churn_pct(S["feeAtivo"], S["feeAviso"] + r)          # redução entra no numerador
        S["churnPctVar"] = churn_pct(S["feeAtivo"] + v, S["feeAviso"] + r)

    tot_atv = round(sum(S["feeAtivo"] for S in squads), 2)
    tot_avi = round(sum(S["feeAviso"] for S in squads), 2)
    tot_var = round(sum(S.get("variavel", 0.0) for S in squads), 2)
    ratio = (tot_var / tot_atv) if tot_atv else 0.0   # rateio uniforme p/ estimar variável por pessoa
    for p in ppl:
        pv = round(p["feeAtivo"] * ratio, 2)
        p["variavel"] = pv
        p["feeAtivoVar"] = round(p["feeAtivo"] + pv, 2)
        p["churnPctVar"] = churn_pct(p["feeAtivo"] + pv, p["feeAviso"])

    tot_red = round(sum(S.get("reducao", 0.0) for S in squads), 2)
    totals = {"feeAtivo": tot_atv, "feeAviso": tot_avi, "variavel": tot_var, "reducao": tot_red,
              "feeAtivoVar": round(tot_atv + tot_var, 2),
              "nAtivo": sum(S["nAtivo"] for S in squads), "nAviso": sum(S["nAviso"] for S in squads),
              "nChurn": sum(S["nChurn"] for S in squads), "churnPct": churn_pct(tot_atv, tot_avi + tot_red),
              "churnPctVar": churn_pct(tot_atv + tot_var, tot_avi + tot_red)}

    # ---- Projeção: cliente em aviso hoje sai ~30 dias depois (modelo da planilha "Projetos 01/MM").
    # TODO cliente em aviso entra na projeção — mesmo sem data do aviso (vai p/ "sem-data"), para casar
    # exatamente com o churn/carteira das pessoas (senão a projeção "não busca todos os churns").
    projection = {}
    for c in clients:
        if c["grp"] != "aviso":
            continue
        dt = None
        if c.get("aviso"):
            try:
                dt = datetime.date.fromisoformat(c["aviso"]) + datetime.timedelta(days=30)
            except Exception:
                dt = None
        key = ("%04d-%02d" % (dt.year, dt.month)) if dt else "sem-data"
        pr = projection.setdefault(key, {"mes": key, "n": 0, "fee": 0.0, "clients": []})
        pr["n"] += 1; pr["fee"] += c["fee"]
        pr["clients"].append({"name": c["name"], "squad": c["squad"], "fee": round(c["fee"], 2),
                              "churnEm": dt.isoformat() if dt else None,
                              "account": c.get("account"), "accountUid": c.get("accountUid"),
                              "gestor": c.get("gestor"), "gestorUid": c.get("gestorUid"),
                              "accountUids": c.get("accountUids") or [], "gestorUids": c.get("gestorUids") or []})
    # ordena por mês; "sem-data" por último
    projection = [dict(v, fee=round(v["fee"], 2)) for v in sorted(projection.values(),
                  key=lambda x: ("9999-99" if x["mes"] == "sem-data" else x["mes"]))]

    return {"totals": totals, "squads": squads, "people": ppl, "clients": clients,
            "squadOrder": SQUAD_ALL, "projection": projection, "variavelMes": (variavel or {}).get("mes"),
            "reducoes": reducoes_list or []}

def record_fee_snapshot(churn, today):
    hist = _load(FEEHIST, {})
    hist[today.isoformat()] = {
        "feeAtivo": churn["totals"]["feeAtivo"], "feeAviso": churn["totals"]["feeAviso"],
        "churnPct": churn["totals"]["churnPct"],
        "bySquad": {S["squad"]: S["feeAtivo"] for S in churn["squads"]},
        # carteira ATIVA por squad e por pessoa (acc/ges) — base do bônus (fee do fechamento do mês)
        "byPerson": {str(p["uid"]): {"acc": p.get("accFee", 0.0), "ges": p.get("gesFee", 0.0), "tot": p["feeAtivo"]}
                     for p in churn.get("people", [])},
    }
    json.dump(hist, open(FEEHIST, "w", encoding="utf-8"), ensure_ascii=False)
    return hist

def bonus_base(fee_history, today):
    """Base do bônus = fee ativo da carteira no ÚLTIMO DIA DO MÊS PASSADO (só projetos ativos).
    Pega o snapshot mais recente que caia no mês anterior; se não houver ainda, sinaliza indisponível."""
    y, mo = today.year, today.month
    py, pm = (y - 1, 12) if mo == 1 else (y, mo - 1)
    prefix = "%04d-%02d" % (py, pm)
    dias = sorted(d for d in (fee_history or {}) if isinstance(d, str) and d.startswith(prefix))
    if not dias:
        return {"mes": prefix, "disponivel": False, "bySquad": {}, "byPerson": {}}
    snap = fee_history[dias[-1]]
    return {"mes": prefix, "dia": dias[-1], "disponivel": True,
            "bySquad": snap.get("bySquad", {}) or {}, "byPerson": snap.get("byPerson", {}) or {}}

def record_churn_history(churn, hist, today):
    """Grava o churn% de cada squad no mês atual (matriz churn_history), acumulando com o tempo.
    Squads novos (ex.: FENIX) passam a ter série própria a partir de agora. Sobrescreve só o mês corrente."""
    hist.setdefault("squads", [])
    hist.setdefault("meses", {})
    key = "%04d-%02d" % (today.year, today.month)
    month = hist["meses"].setdefault(key, {})
    order = [s for s in hist["squads"] if s not in ("TOTAL", "—")]
    month.pop("—", None)   # "—" = clientes sem squad; não é um squad de verdade
    for S in churn["squads"]:
        if S["squad"] == "—":
            continue
        month[S["squad"]] = S["churnPct"]
        if S["squad"] not in order:
            order.append(S["squad"])
    month["TOTAL"] = churn["totals"]["churnPct"]
    hist["squads"] = order + ["TOTAL"]
    # churn% por pessoa no mês (série própria de cada um — passa a acumular do mês atual em diante)
    hist.setdefault("pessoas", {})
    hist.setdefault("pessoasNomes", {})
    pmes = hist["pessoas"].setdefault(key, {})
    for p in churn.get("people", []):
        if (p.get("nAtivo", 0) + p.get("nAviso", 0)) == 0:
            continue
        uid = str(p["uid"])
        pmes[uid] = p["churnPct"]
        hist["pessoasNomes"][uid] = p.get("name") or hist["pessoasNomes"].get(uid) or uid
    json.dump(hist, open(os.path.join(DATA, "churn_history.json"), "w", encoding="utf-8"), ensure_ascii=False)
    return hist

# ------------------------------------------------------------------ roster dos times (dinâmico)
def _order_teams(teams):
    """Ordena os times na ordem canônica dos squads (ADFORCE, G.O.A.T, ...)."""
    return [s for s in SQUAD_ALL if s in teams] + sorted(t for t in teams if t not in SQUAD_ALL)

def roster_from_empresas(empresas):
    """Deriva {uid: {"name","teams":set,"roles":set}} da lista de clientes:
    cada Account/Gestor de um cliente entra no time (squad) daquele cliente."""
    r = {}
    for t in empresas:
        if not is_company(t):
            continue
        squad = _cf_squad(t) or "—"
        if squad == "—" or squad in EXCLUDE_SQUADS:
            continue
        for cid, role in ((CF_ACCOUNT, "Account"), (CF_GESTOR, "Gestor de Tráfego")):
            for u in _cf_users(t, cid):
                e = r.setdefault(u["uid"], {"name": "", "teams": set(), "roles": set()})
                if u.get("name") and not e["name"]:
                    e["name"] = u["name"]
                e["teams"].add(squad)
                e["roles"].add(role)
    return r

def build_roster(empresas):
    """Monta o roster de Tarefas: os 14 membros curados (mantêm nome/função/time e ordem) +
    todos os Account/Gestor de cada squad vindos da lista de clientes. Pessoas em mais de um
    squad aparecem em cada um (campo 'teams'); 'team' é o time principal (p/ avatar/label)."""
    derived = roster_from_empresas(empresas)
    roster, order = {}, 0
    for u in MEMBER_ORDER:                     # 1) curados primeiro (preserva ordem e função)
        name, team, role = MEMBERS[u]
        teams = {team} | (derived.get(u, {}).get("teams") or set())
        roster[u] = {"uid": u, "name": name, "team": team, "role": role,
                     "teams": _order_teams(teams), "order": order}
        order += 1
    for u, e in derived.items():               # 2) demais pessoas da lista de clientes
        if u in roster:
            continue
        teams = _order_teams(e["teams"])
        both = ("Account" in e["roles"]) and ("Gestor de Tráfego" in e["roles"])
        role = "Account / Gestor" if both else ("Account" if "Account" in e["roles"]
               else ("Gestor de Tráfego" if e["roles"] else "—"))
        roster[u] = {"uid": u, "name": e["name"] or str(u), "team": teams[0] if teams else "—",
                     "role": role, "teams": teams, "order": order}
        order += 1
    return roster

# ------------------------------------------------------------------ analyze
def analyze(tasks, record=False):
    today = datetime.datetime.now(TZ).date()
    empresas = _load(os.path.join(DATA, "empresas.json"), [])   # base p/ churn e p/ roster dos times
    roster = build_roster(empresas)
    roster_ids = set(roster)
    if record:
        record_postponements(tasks, today, roster_ids)   # registra adiamentos de prazo vs. rodada anterior
    overdue, malformed, done, today_tasks, created, seen = [], [], [], [], [], set()
    byid = {t["id"]: t for t in tasks}
    min_day = today
    for t in tasks:
        if t["id"] in seen:
            continue
        seen.add(t["id"])
        lst = (t.get("list") or {}).get("name") or "—"
        if lst in EXCLUDE_LISTS:
            continue
        due = to_date(t.get("due_date"))
        closed = to_date(t.get("date_closed")) if is_closed(t) else None
        assignees = [a["id"] for a in t.get("assignees", [])]
        members_assigned = [i for i in assignees if i in roster_ids]

        if closed:
            # concluída (no prazo x atraso) — guardamos detalhes para listar
            late = 1 if (due and closed > due) else 0
            nod = 1 if not due else 0
            proj = resolve_project(t, byid)
            for uid in members_assigned:
                done.append({"uid": uid, "id": t["id"], "name": t.get("name", ""), "list": lst,
                             "project": proj, "day": closed.isoformat(), "late": late, "noDue": nod})
                if closed < min_day: min_day = closed
        else:
            # aberta com prazo, atribuída a um membro → atraso (vencido) ou "para hoje" (vence hoje)
            if due and members_assigned:
                pr = (t.get("priority") or {}).get("priority") if isinstance(t.get("priority"), dict) else None
                proj = resolve_project(t, byid)
                st = (t.get("status") or {}).get("status", "")
                if due < today:
                    bucket = "campanha" if lst in NAO_ACAO_LISTS else "acao"
                    for uid in members_assigned:
                        overdue.append({
                            "id": t["id"], "name": t.get("name", ""), "status": st,
                            "priority": pr, "list": lst, "project": proj,
                            "due": due.strftime("%d/%m/%y"), "days": (today - due).days,
                            "bucket": bucket, "uid": uid,
                        })
                elif due == today:
                    for uid in members_assigned:
                        today_tasks.append({
                            "id": t["id"], "name": t.get("name", ""), "status": st,
                            "priority": pr, "list": lst, "project": proj, "uid": uid,
                        })
            # mal cadastradas: só tarefas de topo abertas, nas listas de trabalho de cliente
            if not t.get("parent") and lst in MALFORMED_LISTS:
                problems = []
                if not assignees:
                    problems.append("sem_responsavel")
                if due is None and assignees and lst in DUE_EXPECTED_LISTS:
                    problems.append("sem_prazo")
                if problems:
                    acc_ids = member_ids_from_cf(t, CF_ACCOUNT)
                    ges_ids = member_ids_from_cf(t, CF_GESTOR)
                    account = next((roster[i]["name"] for i in acc_ids if i in roster_ids), None)
                    gestor = next((roster[i]["name"] for i in ges_ids if i in roster_ids), None)
                    team = squad_team(t)
                    # provável dono: 1) responsável do time, 2) Account, 3) Gestor
                    prob = (members_assigned[0] if members_assigned else None) \
                        or next((i for i in acc_ids if i in roster_ids), None) \
                        or next((i for i in ges_ids if i in roster_ids), None)
                    if prob and not team:
                        team = roster[prob]["team"]
                    cd0 = to_date(t.get("date_created"))
                    malformed.append({
                        "id": t["id"], "name": t.get("name", ""), "list": lst,
                        "problems": problems, "uid": prob, "account": account, "gestor": gestor,
                        "team": team, "created": cd0.strftime("%d/%m/%y") if cd0 else "",
                    })

        # comportamento: criação (por quem criou, se for do time) — vale para aberta ou concluída
        cr = (t.get("creator") or {}).get("id")
        cd = to_date(t.get("date_created"))
        if cr in roster_ids and cd:
            created.append({"uid": cr, "day": cd.isoformat()})
            if cd < min_day: min_day = cd

    avatars = _load(os.path.join(DATA, "avatars.json"), {})
    members = [{"uid": r["uid"], "name": r["name"], "team": r["team"], "teams": r["teams"],
                "role": r["role"], "avatar": avatars.get(str(r["uid"]))}
               for r in sorted(roster.values(), key=lambda x: x["order"])]
    postpones = aggregate_postponements()

    # ---- controle de churn (lista Gestão de empresas) — empresas já carregada no topo ----
    # snapshot manual da planilha (histórico churn% por mês + variável do mês). Editáveis à mão.
    churn_history = _load(os.path.join(DATA, "churn_history.json"), {})
    variavel = _load(os.path.join(DATA, "churn_variavel.json"), {})
    # lançamentos avulsos (compartilhados no repo): variável e reduções vinculadas a clientes.
    lanc = _load(os.path.join(DATA, "lancamentos.json"), {"variaveis": [], "reducoes": []})
    mes_atual = "%04d-%02d" % (today.year, today.month)
    def _lanc_mes(e):
        return (e.get("mes") or mes_atual) == mes_atual
    # variável por squad = snapshot da planilha + lançamentos do mês atual
    vbys = dict((variavel or {}).get("bySquad", {}))
    for e in lanc.get("variaveis", []):
        if not _lanc_mes(e):
            continue
        s = e.get("squad") or "—"
        cur = float((vbys.get(s) or {}).get("variavel") or 0.0)
        vbys[s] = {"variavel": round(cur + float(e.get("valor") or 0.0), 2)}
    variavel = dict(variavel or {}, bySquad=vbys, mes=(variavel or {}).get("mes"))
    # reduções por squad (mês atual) + lista p/ exibição
    red_by, red_list = {}, []
    for e in lanc.get("reducoes", []):
        if not _lanc_mes(e):
            continue
        s = e.get("squad") or "—"
        red_by[s] = round(float(red_by.get(s, 0.0)) + float(e.get("valor") or 0.0), 2)
        red_list.append({"cliente": e.get("cliente"), "squad": s, "valor": round(float(e.get("valor") or 0.0), 2),
                         "motivo": e.get("motivo"), "data": e.get("data"), "mes": e.get("mes") or mes_atual})
    churn = build_churn(empresas, variavel, red_by, red_list)
    if record:
        record_fee_snapshot(churn, today)
        record_churn_history(churn, churn_history, today)   # acumula churn% por squad no mês atual
    fee_history = _load(FEEHIST, {})
    churn["bonusBase"] = bonus_base(fee_history, today)     # bônus usa o fee do fechamento do mês passado

    model = {
        "generated": today.strftime("%d/%m/%Y"),
        "window": {"from": min_day.isoformat(), "to": today.isoformat()},
        "members": members,
        "overdue": overdue,
        "malformed": malformed,
        "today": today_tasks,
        "done": done,
        "created": created,
        "postpones": postpones,
        "churn": churn,
        "feeHistory": fee_history,
        "churnHistory": churn_history,
        "lancamentos": {"variaveis": lanc.get("variaveis", []), "reducoes": lanc.get("reducoes", []), "mesAtual": mes_atual},
    }
    json.dump(model, open(os.path.join(HERE, "model.json"), "w", encoding="utf-8"), ensure_ascii=False)
    print(f"\nmodel.json: {len(overdue)} atrasos · {len(today_tasks)} p/ hoje · {len(done)} concluídas · "
          f"{len(malformed)} mal cadastradas · {len(postpones)} com adiamento · janela {min_day} → {today}")
    print(f"churn: {len(churn['clients'])} empresas · fee ativo R$ {churn['totals']['feeAtivo']:.0f} · "
          f"em aviso R$ {churn['totals']['feeAviso']:.0f} · churn {churn['totals']['churnPct']}% · "
          f"{len(churn['squads'])} squads · {len(churn['people'])} pessoas")
    return model

# ------------------------------------------------------------------ main
def main():
    if "--render-only" in sys.argv:
        model = json.load(open(os.path.join(HERE, "model.json"), encoding="utf-8"))
    elif "--no-fetch" in sys.argv:
        tasks = json.load(open(os.path.join(DATA, "tasks.json"), encoding="utf-8"))
        model = analyze(tasks, record=False)   # sem dados novos: não registra adiamentos
    else:
        token = get_token()
        try:
            tasks = fetch_all(token)
        except ApiError as e:
            msg = str(e)
            if "401" in msg or "OAUTH" in msg.upper():
                sys.exit("\nERRO: token inválido ou expirado (401). Confira o conteúdo de token.txt.\n" + msg)
            sys.exit("\nERRO ao baixar do ClickUp:\n" + msg)
        model = analyze(tasks, record=True)    # dados frescos: compara com a rodada anterior

    import render
    open(os.path.join(HERE, "dashboard.html"), "w", encoding="utf-8").write(render.render(model))
    print("dashboard.html gerado. Abra no navegador.")

if __name__ == "__main__":
    main()

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
# Listas varridas para detectar tarefas mal cadastradas (id -> nome).
SCAN_LISTS = {
    "900702240138": "Gestão de Projetos",
    "901109318541": "Processos de Artes",
    "901112732707": "Planejamento e Gestão de CRM",
    "901111244864": "Envio de NPS",
    "901113455695": "Otimização de Campanhas",
    "901109113085": "Kickoff",
    "901109113867": "Entrada do cliente",
    "901109112970": "Agenda de clientes",
    "901113655081": "Coleta de indicações",
    "901113446899": "Onboarding com o Head",
}
# "Sem prazo" só é erro em listas de entregável datado (evita marcar card de cliente /
# reunião recorrente / template de kickoff, que normalmente não têm prazo).
DUE_EXPECTED_LISTS = {"Processos de Artes", "Planejamento e Gestão de CRM", "Otimização de Campanhas"}

# ---- Campos personalizados (descobertos na lista Gestão de Projetos) ----
CF_ACCOUNT = "89b1f5f2-cbd4-4f83-a26e-35237a3979b9"
CF_GESTOR  = "109e26b9-be03-4c1c-bfe6-8ce55f893d4d"
CF_SQUAD   = "41162abd-5add-4ba8-8021-8e429437f907"
SQUAD_OPTION_TEAM = {  # option_id -> time
    "e7381c3d-7fa2-49dc-b751-3119a12480b6": "E-SCALE",
    "5b22d724-ccb2-4d9f-a4d9-f722e60387c5": "FENIX",
}

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
    print("Baixando tarefas das listas do time (abertas + concluídas)...")
    tasks, seen = [], set()
    for lid, lname in SCAN_LISTS.items():
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
    return tasks

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
                if u.get("id") in MEMBERS and u.get("profilePicture"):
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
            return SQUAD_OPTION_TEAM.get(str(f["value"]))
    return None

def resolve_project(t, byid):
    """Cliente/projeto da tarefa: sobe a hierarquia até o card raiz (o card do cliente).
    Se for uma tarefa de topo (sem pai), tenta a tag [XXX] no início do nome."""
    seen, cur = set(), t
    while cur.get("parent") and cur["parent"] in byid and cur["parent"] not in seen:
        seen.add(cur["parent"])
        cur = byid[cur["parent"]]
    if cur is not t:
        return (cur.get("name") or "").strip()
    m = re.match(r"\s*\[([^\]]+)\]", t.get("name", "") or "")
    return m.group(1).strip() if m else ""

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

def record_postponements(tasks, today):
    prev = _load(STATE, {})          # {id: {"due": "YYYY-MM-DD", ...}}
    log = _load(PLOG, [])
    logged = {(e["id"], e["at"], e["to"]) for e in log}  # evita duplicar na mesma rodada
    cur = {}
    for t in tasks:
        lst = (t.get("list") or {}).get("name") or "—"
        if lst in EXCLUDE_LISTS or is_closed(t):
            continue
        due = to_date(t.get("due_date"))
        uids = [a["id"] for a in t.get("assignees", []) if a["id"] in MEMBERS]
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

# ------------------------------------------------------------------ analyze
def analyze(tasks, record=False):
    today = datetime.datetime.now(TZ).date()
    if record:
        record_postponements(tasks, today)   # registra adiamentos de prazo vs. rodada anterior
    overdue, malformed, events, seen = [], [], [], set()
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
        members_assigned = [i for i in assignees if i in MEMBERS]

        if closed:
            # comportamento: conclusão (no prazo x atraso)
            late = 1 if (due and closed > due) else 0
            nod = 1 if not due else 0
            for uid in members_assigned:
                events.append({"uid": uid, "kind": "done", "day": closed.isoformat(), "late": late, "noDue": nod})
                if closed < min_day: min_day = closed
        else:
            # em atraso: aberta, prazo vencido, atribuída a um membro
            if due and due < today and members_assigned:
                bucket = "campanha" if lst in NAO_ACAO_LISTS else "acao"
                pr = (t.get("priority") or {}).get("priority") if isinstance(t.get("priority"), dict) else None
                proj = resolve_project(t, byid)
                for uid in members_assigned:
                    overdue.append({
                        "id": t["id"], "name": t.get("name", ""),
                        "status": (t.get("status") or {}).get("status", ""),
                        "priority": pr, "list": lst, "project": proj,
                        "due": due.strftime("%d/%m/%y"), "days": (today - due).days,
                        "bucket": bucket, "uid": uid,
                    })
            # mal cadastradas: só tarefas de topo abertas (subtarefa sem dono/prazo herda do pai)
            if not t.get("parent"):
                problems = []
                if not assignees:
                    problems.append("sem_responsavel")
                if due is None and assignees and lst in DUE_EXPECTED_LISTS:
                    problems.append("sem_prazo")
                if problems:
                    acc_ids = member_ids_from_cf(t, CF_ACCOUNT)
                    ges_ids = member_ids_from_cf(t, CF_GESTOR)
                    account = next((MEMBERS[i][0] for i in acc_ids if i in MEMBERS), None)
                    gestor = next((MEMBERS[i][0] for i in ges_ids if i in MEMBERS), None)
                    team = squad_team(t)
                    # provável dono: 1) responsável do time, 2) Account, 3) Gestor
                    prob = (members_assigned[0] if members_assigned else None) \
                        or next((i for i in acc_ids if i in MEMBERS), None) \
                        or next((i for i in ges_ids if i in MEMBERS), None)
                    if prob and not team:
                        team = MEMBERS[prob][1]
                    cd0 = to_date(t.get("date_created"))
                    malformed.append({
                        "id": t["id"], "name": t.get("name", ""), "list": lst,
                        "problems": problems, "uid": prob, "account": account, "gestor": gestor,
                        "team": team, "created": cd0.strftime("%d/%m/%y") if cd0 else "",
                    })

        # comportamento: criação (por quem criou, se for do time) — vale para aberta ou concluída
        cr = (t.get("creator") or {}).get("id")
        cd = to_date(t.get("date_created"))
        if cr in MEMBERS and cd:
            events.append({"uid": cr, "kind": "created", "day": cd.isoformat(), "late": 0, "noDue": 0})
            if cd < min_day: min_day = cd

    avatars = _load(os.path.join(DATA, "avatars.json"), {})
    members = [{"uid": u, "name": MEMBERS[u][0], "team": MEMBERS[u][1], "role": MEMBERS[u][2],
                "avatar": avatars.get(str(u))} for u in MEMBER_ORDER]
    postpones = aggregate_postponements()
    model = {
        "generated": today.strftime("%d/%m/%Y"),
        "window": {"from": min_day.isoformat(), "to": today.isoformat()},
        "members": members,
        "overdue": overdue,
        "malformed": malformed,
        "events": events,
        "postpones": postpones,
    }
    json.dump(model, open(os.path.join(HERE, "model.json"), "w", encoding="utf-8"), ensure_ascii=False)
    print(f"\nmodel.json: {len(overdue)} atrasos · {len(malformed)} mal cadastradas · {len(events)} eventos "
          f"· {len(postpones)} tarefa(s) com adiamento · janela {min_day} → {today}")
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

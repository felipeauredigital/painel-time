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
import zipfile, io, xml.etree.ElementTree as ET

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

# ---- Roster dos times em TAREFAS: vem da lista "Gestão de Projetos" (não da de empresas) ----
PROJETOS_LIST = "900702240138"   # lista "Gestão de Projetos" (espaço Operacional)
# Só o grupo "Fechado" (status FINALIZADO, type="closed") não define time. Todos os outros contam —
# EM PROGRESSO, EM BARREIRA, ATIVO, PROJETO PAUSADO, AVISO e RECISÃO. (ex.: ADFORCE do Lucas = Finalizado)

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
ST_ATIVO   = {"ativo"}                                           # carteira ativa (base) — só ativo
ST_ONBOARD = {"processo de entrada", "aguardando inicio"}       # entrando (ainda não na base)
# Churn = status de churn. O MÊS de cada um vem da Data de Saída (não do status). Aviso/rescisão/
# pendência adm/inadimplente = saindo; finalizado = já saiu (aviso acabou). Regra: STATUS + DATA DE SAÍDA.
ST_CHURN   = {"aviso", "rescisão", "pendência adm", "inadimplente", "finalizado"}
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

# ------------------------------------------------------------------ planilha Google (variável + reduções)
# Fonte compartilhada: o time preenche a planilha; o painel lê dela a cada rodada.
# Abas: "{TIME} - Churn" (reduções) e "{TIME} - Variável" (comissão). Blocos por mês.
PLANILHA_ID = "1rObxF8ftyxvV1c2mtM0zyip22YVFf45OO-7Wyg-1Ixc"
PLANILHA_CACHE = os.path.join(DATA, "planilha_cache.json")
_XNS = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
_XRNS = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}"
MESES_PT = {"JANEIRO": 1, "FEVEREIRO": 2, "MARÇO": 3, "MARCO": 3, "ABRIL": 4, "MAIO": 5, "JUNHO": 6,
            "JULHO": 7, "AGOSTO": 8, "SETEMBRO": 9, "OUTUBRO": 10, "NOVEMBRO": 11, "DEZEMBRO": 12}

def _plan_num(x):
    if x in (None, ""):
        return 0.0
    s = str(x).replace("R$", "").strip()
    if "," in s and "." in s:
        s = s.replace(".", "").replace(",", ".")
    elif "," in s:
        s = s.replace(",", ".")
    try:
        return float(s)
    except Exception:
        return 0.0

def parse_planilha_xlsx(xlsx_bytes):
    """Lê o .xlsx da planilha (stdlib) e devolve {reducoes:[...], variaveis:[...]}.
    Time = nome da aba antes de ' - '; mês = título do bloco; valor de churn = coluna Valor;
    valor de variável = coluna 'Valor da Comissão'. Ignora cabeçalhos, 'Total do mês' e exemplos."""
    z = zipfile.ZipFile(io.BytesIO(xlsx_bytes))
    ss = []
    if "xl/sharedStrings.xml" in z.namelist():
        r = ET.fromstring(z.read("xl/sharedStrings.xml"))
        for si in r.findall(_XNS + "si"):
            ss.append("".join(t.text or "" for t in si.iter(_XNS + "t")))
    wb = ET.fromstring(z.read("xl/workbook.xml"))
    rels = ET.fromstring(z.read("xl/_rels/workbook.xml.rels"))
    relmap = {r.get("Id"): r.get("Target") for r in rels}
    reducoes, variaveis = [], []
    for s in wb.find(_XNS + "sheets"):
        name = s.get("name") or ""
        parts = name.split(" - ")
        if len(parts) < 2:
            continue
        squad, tipo = parts[0].strip(), parts[1].strip().lower()
        if squad in EXCLUDE_SQUADS:
            continue
        tgt = relmap.get(s.get(_XRNS + "id"))
        if not tgt:
            continue
        path = ("xl/" + tgt) if not tgt.startswith("/") else tgt[1:]
        grid = {}
        for c in ET.fromstring(z.read(path)).iter(_XNS + "c"):
            ref, t, v = c.get("r"), c.get("t"), c.find(_XNS + "v")
            if v is None or not ref:
                continue
            val = ss[int(v.text)] if t == "s" else v.text
            mm = re.match(r"([A-Z]+)(\d+)", ref)
            grid[(int(mm.group(2)), mm.group(1))] = val
        maxrow = max((rc[0] for rc in grid), default=0)
        cur = None
        for row in range(1, maxrow + 1):
            a = (grid.get((row, "A")) or "").strip()
            if not a:
                continue
            mt = re.match(r".*-\s*\d+/([^/]+)/(\d{4})", a.upper())
            if mt:
                mo = MESES_PT.get(mt.group(1).strip())
                cur = ("%s-%02d" % (mt.group(2), mo)) if mo else None
                continue
            al = a.lower()
            if al in ("cliente", "empresa") or al.startswith("total do m") or "exemplo" in al or not cur:
                continue
            if "churn" in tipo:
                val = _plan_num(grid.get((row, "B")))
                if val > 0:
                    reducoes.append({"squad": squad, "mes": cur, "cliente": a, "valor": round(val, 2),
                                     "motivo": (grid.get((row, "C")) or ""), "data": None})
            elif "vari" in tipo:
                val = _plan_num(grid.get((row, "D")))   # Valor da Comissão
                if val > 0:
                    variaveis.append({"squad": squad, "mes": cur, "cliente": a, "valor": round(val, 2)})
    return {"reducoes": reducoes, "variaveis": variaveis}

def fetch_planilha_lancamentos():
    """Baixa a planilha (export xlsx) e lê variável + reduções. Cacheia o último resultado bom;
    se a rede falhar numa rodada, usa o cache (não zera os números)."""
    url = "https://docs.google.com/spreadsheets/d/%s/export?format=xlsx" % PLANILHA_ID
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "painel-time/1.0"})
        data = urllib.request.urlopen(req, timeout=60).read()
        out = parse_planilha_xlsx(data)
        json.dump(out, open(PLANILHA_CACHE, "w", encoding="utf-8"), ensure_ascii=False)
        print("Planilha lida: %d reduções, %d variáveis." % (len(out["reducoes"]), len(out["variaveis"])))
        return out
    except Exception as e:
        print("  [aviso] não consegui ler a planilha (%s); usando cache." % str(e)[:80])
        return _load(PLANILHA_CACHE, {"reducoes": [], "variaveis": []})

# ---------------------------------------------------------------------------
# Fonte de CHURN: planilha "[Controle] Churns e Bonificações".
# O fee ativo continua vindo do ClickUp; daqui vem só o CHURN (saídas por mês/time)
# e a VARIÁVEL. Abas: "{TIME} - Churn" (blocos mensais) e "Aure - Variável".
# ---------------------------------------------------------------------------
CHURN_SHEET_ID = "10M2woH8TCalSE5qqXKZH9sg3JSOqGdPc6zjWwKB8P9g"
CHURN_SHEET_CACHE = os.path.join(DATA, "churn_sheet_cache.json")
_CS_BLOCK = re.compile(r"CONTROLE CHURN\s*-?\s*(?:\d+\s*/\s*)?([A-Za-zçÇ]+)\s*/\s*(\d{4})", re.I)
_CS_MESYEAR = re.compile(r"([A-Za-zçÇ]+)\s*/\s*(\d{4})")   # p/ blocos de variável ("... - JUNHO/2026")
_TAB2SQUAD = {"GOAT": "G.O.A.T"}   # nome da aba -> nome do squad no painel
_MES_ABBR = {"JAN": 1, "FEV": 2, "MAR": 3, "ABR": 4, "MAI": 5, "JUN": 6,
             "JUL": 7, "AGO": 8, "SET": 9, "OUT": 10, "NOV": 11, "DEZ": 12}

def _cs_month(nm):
    nm = (nm or "").upper().strip()
    return MESES_PT.get(nm) or _MES_ABBR.get(nm[:3])

def _cs_num(x):
    if x is None:
        return None
    s = str(x).strip()
    try:
        return float(s)                      # número cru: "6000.0"
    except Exception:
        pass
    s = s.replace("R$", "").replace(" ", "")
    if "," in s:
        s = s.replace(".", "").replace(",", ".")   # BR: 1.700,00
    try:
        return float(s)
    except Exception:
        return None

def _cs_grid(z, path, ss):
    grid = {}
    for c in ET.fromstring(z.read(path)).iter(_XNS + "c"):
        ref, t, v = c.get("r"), c.get("t"), c.find(_XNS + "v")
        if v is None or not ref:
            continue
        val = ss[int(v.text)] if t == "s" else v.text
        mm = re.match(r"([A-Z]+)(\d+)", ref)
        col = 0
        for ch in mm.group(1):
            col = col * 26 + (ord(ch) - 64)
        grid.setdefault(int(mm.group(2)), {})[col - 1] = val
    return grid

def parse_churn_sheet_xlsx(xlsx_bytes):
    """Lê a planilha de churn (stdlib). Retorna:
      {"churns":[{squad,mes,cliente,fee,resp}], "variaveis":[{squad,mes,valor}], "val":[(squad,mes,meu,ref,ok)]}
    - churns: abas '{TIME} - Churn', blocos 'CONTROLE CHURN - .../{mes}/{ano}', coluna Fee Mensal.
      Cada bloco é validado contra a soma/Total da própria planilha (campo 'val').
    - variaveis: aba 'Aure - Variável', coluna 'Valor da Comissão' por Squad/mês."""
    z = zipfile.ZipFile(io.BytesIO(xlsx_bytes))
    ss = []
    if "xl/sharedStrings.xml" in z.namelist():
        r = ET.fromstring(z.read("xl/sharedStrings.xml"))
        for si in r.findall(_XNS + "si"):
            ss.append("".join(t.text or "" for t in si.iter(_XNS + "t")))
    wb = ET.fromstring(z.read("xl/workbook.xml"))
    rels = ET.fromstring(z.read("xl/_rels/workbook.xml.rels"))
    relmap = {r.get("Id"): r.get("Target") for r in rels}
    teamup = set(x.upper() for x in SQUAD_ALL) | {"GOAT", "AURE"}
    churns, variaveis, val_report = [], [], []
    for s in wb.find(_XNS + "sheets"):
        name = (s.get("name") or "").strip()
        parts = name.split(" - ")
        if len(parts) < 2:
            continue
        tab_team, tipo = parts[0].strip(), parts[1].strip().lower()
        tgt = relmap.get(s.get(_XRNS + "id"))
        if not tgt:
            continue
        path = ("xl/" + tgt) if not tgt.startswith("/") else tgt[1:]
        grid = _cs_grid(z, path, ss)
        maxrow = max(grid, default=0)
        heads = [row for row in range(1, maxrow + 1)
                 if _CS_BLOCK.search(str(grid.get(row, {}).get(0, "")))]

        if tipo == "churn":
            squad = _TAB2SQUAD.get(tab_team.upper(), tab_team)
            if squad.upper() == "AURE" or squad in EXCLUDE_SQUADS:
                continue                       # consolidado não entra (evita dobrar)
            for bi, hr in enumerate(heads):
                end = heads[bi + 1] if bi + 1 < len(heads) else maxrow + 1
                m = _CS_BLOCK.search(str(grid.get(hr, {}).get(0, "")))
                mo = MESES_PT.get(m.group(1).upper())
                if not mo:
                    continue
                mes = "%s-%02d" % (m.group(2), mo)
                feecol = respcol = varcol = hdr = None
                for rr in range(hr, min(hr + 4, end)):
                    row = grid.get(rr, {})
                    fc = next((ci for ci, v in row.items() if str(v).strip() == "Fee Mensal"), None)
                    if fc is not None:
                        feecol, hdr = fc, rr
                        respcol = next((ci for ci, v in row.items()
                                        if str(v).strip().lower().startswith("respons")), None)
                        varcol = next((ci for ci, v in row.items()
                                       if str(v).strip() == "Fee Variável"), None)   # churn = Fee Mensal + Fee Variável
                        break
                if feecol is None:
                    continue
                block_sum, sheet_sum, sheet_tot = 0.0, None, None
                for rr in range(hdr + 1, end):
                    cells = grid.get(rr, {})
                    emp = str(cells.get(0, "")).strip()
                    fv = _cs_num(cells.get(feecol))
                    if emp.startswith("Total"):
                        sheet_tot = _cs_num(cells.get(feecol)) or _cs_num(cells.get(1))
                        break
                    if emp.startswith("Clientes Ativos") or emp.startswith("CONTROLE") or emp.upper() in teamup:
                        break
                    if emp == "":
                        if fv is not None and sheet_sum is None:
                            sheet_sum = fv
                        continue
                    if emp in ("Empresa", "M"):
                        continue
                    if fv is not None:
                        vv = _cs_num(cells.get(varcol)) if varcol is not None else None
                        fee_tot = fv + (vv or 0.0)      # churn do cliente = Fee Mensal + Fee Variável (o que está na aba)
                        resp = str(cells.get(respcol, "")).strip() if respcol is not None else ""
                        if resp and not any(ch.isalpha() for ch in resp):   # descarta data/serial na coluna Responsável
                            resp = ""
                        churns.append({"squad": squad, "mes": mes, "cliente": emp,
                                       "fee": round(fee_tot, 2), "resp": resp})
                        block_sum += fee_tot
                ok = any(r is not None and abs(block_sum - r) < 1.5 for r in (sheet_tot, sheet_sum))
                ref = sheet_tot if sheet_tot is not None else sheet_sum   # Total Churn (Fee Mensal + Fee Variável)
                val_report.append((squad, mes, round(block_sum, 2), ref, ok))

        elif tipo.startswith("vari"):
            # blocos da variável: "Controle Variável - JUNHO/2026" (ou "CONTROLE CHURN - .../mês/ano")
            vheads = [row for row in range(1, maxrow + 1)
                      if "controle" in str(grid.get(row, {}).get(0, "")).lower()
                      and _CS_MESYEAR.search(str(grid.get(row, {}).get(0, "")))]
            for bi, hr in enumerate(vheads):
                end = vheads[bi + 1] if bi + 1 < len(vheads) else maxrow + 1
                m = _CS_MESYEAR.search(str(grid.get(hr, {}).get(0, "")))
                mo = _cs_month(m.group(1))
                if not mo:
                    continue
                mes = "%s-%02d" % (m.group(2), mo)
                comcol = sqcol = hdr = None
                for rr in range(hr, min(hr + 4, end)):
                    for ci, v in grid.get(rr, {}).items():
                        vs = str(v).strip().lower()
                        if "comiss" in vs:
                            comcol = ci
                        if vs.startswith("squad"):
                            sqcol = ci
                    if comcol is not None:
                        hdr = rr
                        break
                if comcol is None:
                    continue
                for rr in range(hdr + 1, end):
                    cells = grid.get(rr, {})
                    a = str(cells.get(0, "")).strip()
                    if a.lower().startswith("total") or a.startswith("CONTROLE"):
                        break
                    val = _cs_num(cells.get(comcol))
                    if val and val > 0:
                        sq = (str(cells.get(sqcol, "")).strip() if sqcol is not None else "")
                        sq = _TAB2SQUAD.get(sq.upper(), sq) if sq else None
                        if sq and sq not in EXCLUDE_SQUADS:
                            variaveis.append({"squad": sq, "mes": mes, "valor": round(val, 2)})
    return {"churns": churns, "variaveis": variaveis, "val": val_report}

def fetch_churn_sheet():
    """Baixa a planilha de churn (export xlsx), parseia e cacheia. Fallback = cache."""
    url = "https://docs.google.com/spreadsheets/d/%s/export?format=xlsx" % CHURN_SHEET_ID
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "painel-time/1.0"})
        data = urllib.request.urlopen(req, timeout=90).read()
        out = parse_churn_sheet_xlsx(data)
        nb = len(out["val"])
        nok = sum(1 for _, _, _, _, ok in out["val"] if ok)
        json.dump(out, open(CHURN_SHEET_CACHE, "w", encoding="utf-8"), ensure_ascii=False)
        print("Churn (planilha): %d saídas, %d blocos (%d validados), %d variáveis."
              % (len(out["churns"]), nb, nok, len(out["variaveis"])))
        if nb and nok < nb:
            print("  [aviso] %d bloco(s) de churn divergem do total da planilha." % (nb - nok))
        return out
    except Exception as e:
        print("  [aviso] não consegui ler a planilha de churn (%s); usando cache." % str(e)[:80])
        return _load(CHURN_SHEET_CACHE, {"churns": [], "variaveis": [], "val": []})

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

def _nrm_name(s, base=False):
    """Normaliza nome de cliente p/ casar planilha x ClickUp: sem acento, minúsculo, só [a-z0-9].
    base=True descarta o conteúdo entre parênteses — 'Anapi (box, varejo e atacado)' -> 'anapi'."""
    import unicodedata
    s = unicodedata.normalize("NFKD", (s or "")).encode("ascii", "ignore").decode()
    s = s.lower()
    if base:
        s = re.sub(r"\(.*?\)", " ", s)
    s = re.sub(r"[^a-z0-9]+", " ", s)
    return re.sub(r"\s+", " ", s).strip()

def build_churn(empresas, variavel=None, reducoes=None, reducoes_list=None, today=None, sheet_churns=None, home_squad=None):
    """Monta o modelo de churn — FONTE HÍBRIDA:
    - Base (carteira ativa, fee/time/account/gestor) = ClickUp, só clientes 'ativo'.
    - Churn (quem saiu, fee, por mês) = PLANILHA (sheet_churns), atribuído ao mês do bloco:
      mês corrente = churn do mês (entra no %); futuro = projeção; passado = já saiu.
    - churn% do mês = (fee que sai no mês + reduções) / (fee ativo + fee que sai no mês)."""
    today = today or datetime.datetime.now(TZ).date()
    cur_mes = "%04d-%02d" % (today.year, today.month)
    clients, people, sem_data = [], {}, []
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
            p.setdefault("_sqw", {})                       # peso por squad (fallback se a pessoa não estiver no roster)
            p["_sqw"][squad] = p["_sqw"].get(squad, 0) + 1
        if u.get("avatar") and not p.get("avatar"):
            p["avatar"] = u["avatar"]
        return p

    # Índice nome->empresa do ClickUp (TODOS os status, inclusive churn) p/ enriquecer o churn
    # da planilha com Account/Gestor cadastrados na lista Gestão de empresas.
    emp_idx = {}
    def _reg_emp(key, rec):
        if key and len(key) >= 3:
            emp_idx.setdefault(key, []).append(rec)

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
        saida = _cf_date(t, CF_SAIDA)
        aviso = _cf_date(t, CF_AVISO)
        saida_mes = saida[:7] if saida else None
        rec = {"id": t["id"], "acc": acc, "ges": ges, "squad": squad}
        nk = _nrm_name(t.get("name")); bk = _nrm_name(t.get("name"), base=True)
        _reg_emp(nk, rec)
        if bk != nk:
            _reg_emp(bk, rec)
        # STATUS + DATA DE SAÍDA definem o grupo:
        if st in ST_ATIVO:
            grp = "ativo"
        elif st in ST_ONBOARD:
            grp = "onboard"
        elif st in ST_PAUSA:
            grp = "pausa"
        elif st in ST_CHURN:
            continue                                   # churn agora vem da PLANILHA (sheet_churns), não do status
        else:
            grp = "outro"
        clients.append({"id": t["id"], "name": (t.get("name") or "").strip(), "fee": round(fee, 2),
                        "status": st, "grp": grp, "squad": squad, "saidaMes": saida_mes,
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
        elif grp == "aviso":                           # churn deste mês
            S["feeAviso"] += fee; S["nAviso"] += 1
            for u, r in involved:
                p = person(u, r, squad); p["feeAviso"] += fee; p["nAviso"] += 1
        elif grp == "saiu":                            # já saiu (Data de Saída passada)
            S["feeChurn"] += fee; S["nChurn"] += 1
            for u, r in involved:
                p = person(u, r, squad); p["feeChurn"] += fee; p["nChurn"] += 1
        elif grp == "onboard":
            S["nOnboard"] += 1
        elif grp == "semdata":
            sem_data.append({"id": t["id"], "name": (t.get("name") or "").strip(), "squad": squad,
                             "status": st, "fee": round(fee, 2),
                             "account": acc[0]["name"] if acc else None,
                             "gestor": ges[0]["name"] if ges else None})

    # ---- CHURN vindo da PLANILHA (substitui a detecção via status do ClickUp) ----
    # Account/Gestor vêm do CADASTRO DA EMPRESA no ClickUp (emp_idx, casado por nome).
    # Fallback: coluna "Responsável" da planilha (1º nome -> pessoa do mesmo squad).
    STLBL = {"aviso": "aviso", "futuro": "a sair", "saiu": "finalizado"}
    name2uid = {}
    for pp in people.values():
        parts_n = (pp["name"] or "").strip().split()
        fn = parts_n[0].lower() if parts_n else ""
        for sq_ in pp["squads"]:
            name2uid.setdefault((sq_, fn), pp["uid"])

    def _emp_lookup(name, squad):
        """Empresa do ClickUp p/ este cliente da planilha: nome exato -> sem parênteses -> prefixo único."""
        nk = _nrm_name(name); bk = _nrm_name(name, base=True)
        for k in (nk, bk):
            cands = emp_idx.get(k)
            if cands:
                same = [r for r in cands if r["squad"] == squad]
                return (same or cands)[0]
        if len(bk) >= 5:                       # ex.: 'Klosett' x 'Klosett Charm', 'Aleva' x 'Aleva Shoes'
            hits = [r for k, rl in emp_idx.items() if len(k) >= 5
                    and (k.startswith(bk + " ") or bk.startswith(k + " ")) for r in rl]
            same = [r for r in hits if r["squad"] == squad]
            pick = same or hits
            if len({r["id"] for r in pick}) == 1:
                return pick[0]
        return None

    enr = tot = 0
    for c in (sheet_churns or []):
        squad = c.get("squad")
        mes = c.get("mes")
        fee = float(c.get("fee") or 0.0)
        if not squad or squad in EXCLUDE_SQUADS or not mes:
            continue
        tot += 1
        grp = "aviso" if mes == cur_mes else ("futuro" if mes > cur_mes else "saiu")
        resp = (c.get("resp") or "").strip()
        emp = _emp_lookup(c.get("cliente", ""), squad)
        if emp:
            enr += 1
            acc_u = emp["acc"][0] if emp["acc"] else None
            ges_u = emp["ges"][0] if emp["ges"] else None
            involved = [(u, "Account") for u in emp["acc"]] + [(u, "Gestor de Tráfego") for u in emp["ges"]]
        else:
            rfn = resp.split()[0].lower() if resp else ""
            uid = name2uid.get((squad, rfn))
            acc_u = {"uid": uid, "name": resp} if uid else None
            ges_u = None
            involved = [(people[uid], "Account")] if uid in people else []
        clients.append({"id": (emp["id"] if emp else ""), "name": c.get("cliente", ""), "fee": round(fee, 2),
                        "status": STLBL[grp], "grp": grp, "squad": squad, "saidaMes": mes,
                        "account": (acc_u["name"] if acc_u else (resp or None)),
                        "accountUid": (acc_u["uid"] if acc_u else None),
                        "gestor": (ges_u["name"] if ges_u else None),
                        "gestorUid": (ges_u["uid"] if ges_u else None),
                        "accountUids": [u["uid"] for u, r in involved if r == "Account"],
                        "gestorUids": [u["uid"] for u, r in involved if r != "Account"],
                        "entrada": None, "aviso": None, "saida": None, "churnDate": None})
        S = squad_bucket(squad)
        if grp == "aviso":
            S["feeAviso"] += fee; S["nAviso"] += 1
            for u, r in involved:
                p = person(u, r, squad); p["feeAviso"] += fee; p["nAviso"] += 1
        elif grp == "saiu":
            S["feeChurn"] += fee; S["nChurn"] += 1
            for u, r in involved:
                p = person(u, r, squad); p["feeChurn"] += fee; p["nChurn"] += 1
        # grp "futuro" entra só na projeção (via clients[]), não no churn do mês
    if sheet_churns:
        print(f"Churn (planilha): {enr} de {tot} clientes casados com o cadastro do ClickUp (Account/Gestor)")

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
        p["roles"] = sorted(p["roles"])
        # SQUAD DA PESSOA = time de origem (roster de Gestão de Projetos). Uma pessoa = um squad.
        # Fallback (fora do roster): squad predominante da carteira dela; por fim, 1º squad tocado.
        home = (home_squad or {}).get(p["uid"])
        w = p.pop("_sqw", None) or {}
        if home and home not in EXCLUDE_SQUADS:
            p["squads"] = [home]
        elif w:
            p["squads"] = [max(sorted(w), key=lambda s: w[s])]
        else:
            p["squads"] = sorted(p["squads"])[:1]
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

    # ---- Projeção: churn atribuído ao MÊS DA DATA DE SAÍDA (mês corrente + futuros).
    # Cada cliente em status de churn com Data de Saída >= mês corrente entra no mês da sua saída.
    projection = {}
    for c in clients:
        if c["grp"] not in ("aviso", "futuro"):     # mês corrente + meses futuros
            continue
        key = c.get("saidaMes") or "sem-data"
        pr = projection.setdefault(key, {"mes": key, "n": 0, "fee": 0.0, "clients": []})
        pr["n"] += 1; pr["fee"] += c["fee"]
        pr["clients"].append({"name": c["name"], "squad": c["squad"], "fee": round(c["fee"], 2),
                              "churnEm": c.get("saida"), "status": c.get("status"),
                              "account": c.get("account"), "accountUid": c.get("accountUid"),
                              "gestor": c.get("gestor"), "gestorUid": c.get("gestorUid"),
                              "accountUids": c.get("accountUids") or [], "gestorUids": c.get("gestorUids") or []})
    # ordena por mês; "sem-data" por último
    projection = [dict(v, fee=round(v["fee"], 2)) for v in sorted(projection.values(),
                  key=lambda x: ("9999-99" if x["mes"] == "sem-data" else x["mes"]))]

    return {"totals": totals, "squads": squads, "people": ppl, "clients": clients,
            "squadOrder": SQUAD_ALL, "projection": projection, "variavelMes": (variavel or {}).get("mes"),
            "reducoes": reducoes_list or [], "semDataSaida": sem_data, "mesAtual": cur_mes}

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

def roster_from_projetos(tasks):
    """Deriva {uid: {"name","teams":set,"roles":set}} da lista 'Gestão de Projetos':
    para cada PROJETO ATIVO, quem está em Account/Gestor entra no time (squad) daquele projeto.
    Projetos encerrados (finalizado/recisão) não contam — é por isso que o Lucas (Head), que só
    tem projeto ADFORCE finalizado, não cai no ADFORCE."""
    r = {}
    for t in tasks:
        if (t.get("list") or {}).get("id") != PROJETOS_LIST:
            continue
        if ((t.get("status") or {}).get("type")) == "closed":   # só "Fechado" (Finalizado) não conta
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

def build_roster(tasks):
    """Monta o roster de Tarefas: os 14 membros curados (mantêm nome/função/time e ordem) +
    todos os Account/Gestor de cada squad vindos dos PROJETOS ATIVOS (lista Gestão de Projetos).
    Pessoas em mais de um squad aparecem em cada um (campo 'teams'); 'team' é o principal (avatar/label).
    Quem não tem tarefa é removido depois, no analyze."""
    derived = roster_from_projetos(tasks)
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
    roster = build_roster(tasks)   # times de Tarefas: Account/Gestor de cada projeto ATIVO (+ curados)
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
    postpones = aggregate_postponements()
    # roster = todos os Account/Gestor de projetos ATIVOS (+ curados). Ex-funcionário já não entra
    # aqui, pois não é account/gestor de projeto ativo — então não filtramos por "ter tarefa".
    members = [{"uid": r["uid"], "name": r["name"], "team": r["team"], "teams": r["teams"],
                "role": r["role"], "avatar": avatars.get(str(r["uid"]))}
               for r in sorted(roster.values(), key=lambda x: x["order"])]

    # ---- controle de churn (lista Gestão de empresas) ----
    empresas = _load(os.path.join(DATA, "empresas.json"), [])
    churn_history = _load(os.path.join(DATA, "churn_history.json"), {})
    mes_atual = "%04d-%02d" % (today.year, today.month)
    py, pm = (today.year - 1, 12) if today.month == 1 else (today.year, today.month - 1)
    mes_prev = "%04d-%02d" % (py, pm)   # variável deste mês vale na META do mês seguinte
    # FONTE do CHURN: planilha "[Controle] Churns e Bonificações" (o time preenche; o painel lê).
    # Fetch fresco nas rodadas de nuvem (record=True); --no-fetch usa o cache p/ não zerar.
    sheet = fetch_churn_sheet() if record else _load(CHURN_SHEET_CACHE, {"churns": [], "variaveis": [], "val": []})
    # Variável por (mês, squad). Ela é preenchida no início do mês seguinte e vale na bonificação
    # desse mês seguinte → a última disponível é a do mês anterior (mes_prev), que é a operativa agora.
    var_by = {}
    for e in sheet.get("variaveis", []):
        s = e.get("squad") or "—"
        mv = var_by.setdefault(e.get("mes"), {})
        mv[s] = round(float(mv.get(s, 0.0)) + float(e.get("valor") or 0.0), 2)
    var_prev = dict(var_by.get(mes_prev, {}))                       # base da bonificação deste mês
    vbys = {s: {"variavel": v} for s, v in var_prev.items()}       # operativa = última preenchida (mês anterior)
    red_by, red_list = {}, []                                      # reduções já entram como saídas na planilha
    variavel = {"bySquad": vbys, "mes": mes_prev}
    # time de origem de cada pessoa (roster de Gestão de Projetos) → squad único no churn por pessoa
    home_squad = {uid: r.get("team") for uid, r in roster.items() if r.get("team") and r["team"] != "—"}
    churn = build_churn(empresas, variavel, red_by, red_list, today=today,
                        sheet_churns=sheet.get("churns", []), home_squad=home_squad)
    if record:
        record_fee_snapshot(churn, today)
        record_churn_history(churn, churn_history, today)   # acumula churn% por squad no mês atual
    fee_history = _load(FEEHIST, {})
    churn["bonusBase"] = bonus_base(fee_history, today)     # bônus usa o fee do fechamento do mês passado
    churn["bonusBase"]["varBySquad"] = var_prev            # + variável do mês anterior (planilha) na base

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
        # espelho da planilha (leitura): o time preenche na planilha, o painel só mostra
        "lancamentos": {"variaveis": sheet.get("variaveis", []), "reducoes": [],
                        "churns": sheet.get("churns", []), "valida": sheet.get("val", []),
                        "mesAtual": mes_atual, "mesPrev": mes_prev, "fonte": "planilha"},
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

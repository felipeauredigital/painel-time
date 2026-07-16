# Painel do Time — E‑SCALE & FENIX (ClickUp)

Ferramenta local que puxa as tarefas do ClickUp e gera um **dashboard HTML** para o head
acompanhar o time na daily, **pessoa por pessoa**:

- **Tarefas em atraso** por responsável (vencidas e não concluídas), com botão **✓ Fechar**
  para ocultar o que já foi concluído / cliente que saiu (fica salvo no navegador, com desfazer).
- **Comportamento / histórico completo** de cada pessoa: conclusões, **% no prazo**,
  **check em lote** (máx. concluídas num dia), volume criado — com **filtro por datas**.
- **Tarefas mal cadastradas** (sem responsável ou sem prazo), com o **provável dono**
  inferido pelos campos personalizados `Account`, `Gestor de Tráfego` e `Squad`.
- **Visão geral** (ranking por pessoa, onde estão no ClickUp, conclusão no prazo).

Tudo roda **na sua máquina** com o seu token do ClickUp. Nada é enviado para fora.

## Pré‑requisitos
- Python 3.8+ (não precisa instalar nada além — usa só a biblioteca padrão).

## 1) Gerar o token do ClickUp
No ClickUp: **Settings → Apps → API Token → Generate**. Copie o token (começa com `pk_`).

## 2) Informar o token (escolha uma opção)
- **Arquivo** (mais simples): crie um arquivo `.clickup_token` nesta pasta com o token numa linha.
  Ele já está no `.gitignore` — não vai para o git.
- **Variável de ambiente**:
  - Windows (PowerShell): `$env:CLICKUP_TOKEN = "pk_xxx"`
  - Windows (cmd): `set CLICKUP_TOKEN=pk_xxx`
  - Mac/Linux: `export CLICKUP_TOKEN=pk_xxx`

## 3) Rodar
```
python clickup_dash.py
```
Isso baixa tudo, calcula e gera **`dashboard.html`**. Abra o arquivo no navegador
(dê dois cliques). Para atualizar os dados, rode o comando de novo.

### Opções
- `python clickup_dash.py --no-fetch` — reaproveita o que já foi baixado em `data/`
  (recalcula e regera o HTML, sem chamar a API de novo).
- `python clickup_dash.py --render-only` — só regenera o HTML a partir do `model.json`.
- `python render.py --demo` — gera um dashboard de exemplo (dados fictícios) para ver o layout.

## Como funciona (arquivos)
- `clickup_dash.py` — baixa da API do ClickUp, calcula atraso/comportamento/mal cadastradas → `model.json`.
- `render.py` — transforma o `model.json` no `dashboard.html`.
- `data/` — cache das respostas da API (ignorado pelo git).

## Ajustes rápidos (no topo do `clickup_dash.py`)
- `MEMBERS` — pessoas dos times (uid do ClickUp, nome, time, cargo). Edite se o time mudar.
- `EXCLUDE_LISTS` — listas ignoradas (hoje: `Campanhas de Tráfego`, legada).
- `NAO_ACAO_LISTS` — listas que **não** contam como "pendência de ação" (hoje: `Otimização de Campanhas`).
- `SCAN_LISTS` — listas varridas para achar tarefas mal cadastradas.

## Adiamentos de prazo (quantas vezes cada um adia)
A API do ClickUp **não** entrega o histórico de mudanças de prazo. Então o painel guarda um
retrato dos prazos a cada rodada (`data/state.json`) e, na rodada seguinte, registra todo
**adiamento** (prazo empurrado pra frente) num log permanente (`data/postpone_log.json`).
- Aparece por pessoa: um chip **"adiamentos de prazo"**, a seção **"Prazos adiados"** (quantas
  vezes e em quais tarefas, com o de→para) e, na Visão geral, o card **"Mais adiam prazo"**.
- **Começa a contar a partir de agora.** Quanto mais frequente a atualização, mais rico o histórico.
  A 1ª rodada só cria a linha de base (0 adiamentos).

### Rodar sozinho todo dia (Windows)
Para acumular sem esforço, agende o `gerar-painel.bat` no Agendador de Tarefas. Ex. (todo dia 8h):
```
schtasks /Create /SC DAILY /ST 06:00 /TN "Painel Aure" /TR "C:\Users\Felipe\teste\clickup-dashboard\gerar-painel.bat"
```

## Observações
- **Fechar tarefa** oculta apenas no dashboard (salvo no navegador de quem usa). Não altera o
  ClickUp — para fechar de verdade, feche a tarefa lá.
- O **provável dono** das mal cadastradas é uma inferência (campos Account/Gestor/Squad); confira antes de agir.
- Rate limit da API do ClickUp: o script já espera automaticamente se necessário.
- **Acesso do token:** o token só enxerga espaços/pastas de que o usuário dele participa. Se alguma
  lista retornar "sem acesso", o script **pula ela automaticamente** e segue (aparece um aviso). Para
  cobrir tudo, use um token de um usuário com acesso a todos os espaços dos times.
- **Fonte única:** tudo (atraso, comportamento e mal cadastradas) vem do mesmo pull das listas de
  trabalho (`SCAN_LISTS`) com **concluídas incluídas**. Por isso a coleta pode levar alguns minutos.
- **Comportamento** = histórico de tarefas concluídas por pessoa (no prazo x atraso, check em lote,
  criadas). O filtro de datas (atalhos 30/90 dias, Tudo, ou custom + Aplicar) opera sobre esse histórico.

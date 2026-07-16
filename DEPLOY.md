# Colocar o painel online (grátis, só GitHub, sem login)

Como funciona: o **GitHub Actions** roda o script 1×/dia (com o seu token guardado em segredo),
gera o `dashboard.html` e publica no **GitHub Pages**. O endereço fica tipo
`https://SEU_USUARIO.github.io/painel-time/`.

> Requisito do GitHub Pages grátis: o repositório precisa ser **público**. Por isso usamos um
> repositório **dedicado só do painel** (não a pasta inteira `teste`), pra não expor mais nada.
> O seu token do ClickUp NUNCA vai pro repositório (fica como *segredo* e o `token.txt` está no `.gitignore`).

---

## 1) Criar o repositório dedicado (público) com o GitHub Desktop
1. Instale o **GitHub Desktop**: https://desktop.github.com e faça login (crie a conta grátis se precisar).
2. No **Explorer do Windows**, copie a pasta `C:\Users\Felipe\teste\clickup-dashboard` inteira para
   `C:\Users\Felipe\` e renomeie a cópia para **`painel-time`** (fica `C:\Users\Felipe\painel-time`).
   *(Copiar a pasta leva junto os arquivos ocultos `.github` e `.gitignore` — necessários.)*
3. No GitHub Desktop: **File → Add local repository** → escolha `C:\Users\Felipe\painel-time`.
   Ele vai avisar que não é um repositório git → clique em **create a repository** → **Create repository**.
4. Escreva um resumo (ex.: `Painel do time`) e clique **Commit to main**.
5. Clique **Publish repository**:
   - Name: `painel-time`
   - **DESMARQUE** "Keep this code private" (o Pages grátis exige repositório **público**).
   - **Publish repository**.

## 2) Ligar o GitHub Pages
1. Abra o repositório em https://github.com → aba **Settings** → menu esquerdo **Pages**.
2. Em **Build and deployment → Source**, escolha **GitHub Actions**. (Só selecionar; não precisa salvar nada.)

## 3) Colar o segredo do ClickUp
1. Ainda em **Settings** → **Secrets and variables → Actions** → **New repository secret**.
2. Name: `CLICKUP_TOKEN` — Secret: seu token do ClickUp (`pk_...`) → **Add secret**.

> Dica: use um token de uma conta que enxergue **todos os espaços** dos times (senão faltam listas).

## 4) Rodar pela primeira vez
1. Aba **Actions** → se pedir, clique em **I understand… enable**.
2. À esquerda, **"Atualizar painel do time"** → **Run workflow** → **Run workflow** (verde).
3. Aguarde ficar tudo ✅ (uns minutos). No fim, o link aparece no passo "Publicar no GitHub Pages"
   (ou em **Settings → Pages**): algo como `https://SEU_USUARIO.github.io/painel-time/`.

## 5) Compartilhar
Mande esse link para os heads. Pronto — atualiza sozinho todo dia de manhã.

---

### Observações
- **Custo:** zero.
- **Privacidade:** o repositório é público, então o código e os arquivos de dados
  (`data/state.json`, `data/postpone_log.json`, com nomes de tarefas/prazos) ficam visíveis —
  mas isso é o mesmo que o painel já mostra publicamente. Quando quiser **fechar com login**,
  a gente coloca o Cloudflare Access na frente (aí o repo volta a poder ser privado).
- **Frequência:** 1×/dia às 06:00 BRT. Pra atualizar na hora: **Actions → Run workflow**.
- **Adiamentos de prazo:** cada rodada compara com a anterior e acumula (por isso o estado é salvo no repo).

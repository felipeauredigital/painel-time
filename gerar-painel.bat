@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo ============================================
echo   Painel do Time - Aure (ClickUp)
echo ============================================
echo Baixando dados e gerando o painel...
echo.
where python >nul 2>nul
if %errorlevel%==0 (
  python clickup_dash.py
) else (
  py clickup_dash.py
)
if errorlevel 1 (
  echo.
  echo Nao foi possivel gerar. Confira o passo do token.txt acima.
  pause
  exit /b 1
)
echo.
echo Abrindo o painel no navegador...
start "" "dashboard.html"
echo Pronto! Para atualizar depois, e so dar duplo-clique aqui de novo.
pause

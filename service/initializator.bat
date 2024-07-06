@echo off
REM Abrir a pasta "api-bet-sign" no Desktop
cd "%USERPROFILE%\Desktop\api-bet-sign"

REM Ativar o ambiente virtual
call .venv\Scripts\activate

REM Entrar na subpasta "api"
cd api

REM Abrir um terminal e executar 'flask run'
start cmd /k "flask run"

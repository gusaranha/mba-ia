@echo off
REM Script de Setup do Git - Windows
REM Configura Git pela primeira vez no seu computador

echo =========================================
echo    Setup do Git - Aula 4
echo =========================================
echo.

REM Verificar se Git está instalado
where git >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo X Git nao esta instalado!
    echo.
    echo Por favor, instale o Git primeiro:
    echo   - Baixe em: https://git-scm.com/downloads
    echo   - Ou use: winget install Git.Git
    pause
    exit /b 1
)

for /f "tokens=*" %%i in ('git --version') do set GIT_VERSION=%%i
echo V Git encontrado: %GIT_VERSION%
echo.

REM Verificar se já está configurado
git config --global user.name >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    for /f "tokens=*" %%i in ('git config --global user.name') do set GIT_NAME=%%i
    for /f "tokens=*" %%i in ('git config --global user.email') do set GIT_EMAIL=%%i
    
    echo V Git ja esta configurado:
    echo    Nome: %GIT_NAME%
    echo    Email: %GIT_EMAIL%
    echo.
    
    set /p RECONFIG="Deseja reconfigurar? (s/N): "
    if /i not "%RECONFIG%"=="s" (
        echo Setup concluido!
        pause
        exit /b 0
    )
    echo.
)

REM Configurar nome
echo Configurando seu perfil Git...
echo.
set /p NOME="Digite seu nome completo: "
git config --global user.name "%NOME%"

REM Configurar email
set /p EMAIL="Digite seu email: "
git config --global user.email "%EMAIL%"

REM Configurações adicionais recomendadas
echo.
echo Aplicando configuracoes recomendadas...
git config --global init.defaultBranch main
git config --global core.editor "code --wait"
git config --global pull.rebase false

echo.
echo =========================================
echo V Setup concluido com sucesso!
echo =========================================
echo.

for /f "tokens=*" %%i in ('git config --global user.name') do set FINAL_NAME=%%i
for /f "tokens=*" %%i in ('git config --global user.email') do set FINAL_EMAIL=%%i

echo Suas configuracoes:
echo   Nome: %FINAL_NAME%
echo   Email: %FINAL_EMAIL%
echo.
echo Proximos passos:
echo   1. Navegue ate exemplo-inicial/
echo   2. Execute: git log --oneline
echo   3. Explore o historico de commits!
echo.

pause

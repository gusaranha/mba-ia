@echo off
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
    echo Prepare o ambiente seguindo o README antes de iniciar a loja.
    pause
    exit /b 1
)
echo Abra http://localhost:5000 no navegador.
echo Para encerrar, pressione Ctrl+C neste terminal.
".venv\Scripts\python.exe" app.py
pause

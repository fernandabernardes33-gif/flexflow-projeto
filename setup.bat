@echo off
echo ============================================
echo  SIGIT - Instalacao inicial
echo ============================================

echo Verificando Python...
python --version >nul 2>&1
if errorlevel 1 (
    py --version >nul 2>&1
    if errorlevel 1 (
        echo ERRO: Python nao encontrado!
        echo Baixe em: https://www.python.org/downloads/
        echo Durante a instalacao, marque "Add Python to PATH"
        pause & exit /b 1
    )
)

echo [1/4] Criando venv...
cd /d %~dp0backend
python -m venv venv 2>nul || py -m venv venv
call venv\Scripts\activate
python -m pip install --upgrade pip
pip install wheel
echo.

echo [2/4] Instalando dependencias do backend...
pip install --prefer-binary -r requirements.txt
echo.

echo [3/4] Populando banco de dados...
python seed.py
call venv\Scripts\deactivate
cd /d %~dp0
echo.

echo [4/4] Instalando dependencias do frontend...
cd /d %~dp0frontend
npm install
cd /d %~dp0
echo.

echo ============================================
echo  Instalacao concluida! Execute: iniciar.bat
echo  Login: admin@aussistencia.com / admin123
echo ============================================
pause

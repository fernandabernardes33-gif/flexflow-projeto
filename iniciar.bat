@echo off
echo ============================================
echo  AUssistencia - Iniciando servicos
echo  Backend:  http://localhost:8000
echo  Frontend: http://localhost:5173
echo  Login:    admin@aussistencia.com / admin123
echo ============================================

echo Iniciando backend...
start "AUssistencia - Backend" cmd /k "cd /d %~dp0backend && venv\Scripts\activate && uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"

timeout /t 3 /nobreak >nul

echo Iniciando frontend...
start "AUssistencia - Frontend" cmd /k "cd /d %~dp0frontend && npm run dev"

timeout /t 4 /nobreak >nul
start http://localhost:5173

@echo off
echo ╔════════════════════════════════════════════╗
echo ║  QuantaStrike Chat API Server             ║
echo ║  Запуск на http://localhost:8000          ║
echo ╚════════════════════════════════════════════╝
echo.

REM Проверить Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python не найден. Пожалуйста, установите Python.
    pause
    exit /b 1
)

REM Проверить requirements.txt
if not exist requirements.txt (
    echo ❌ requirements.txt не найден.
    pause
    exit /b 1
)

REM Установить зависимости если их нет
python -c "import fastapi" >nul 2>&1
if errorlevel 1 (
    echo 📦 Установка зависимостей...
    pip install -r requirements.txt
)

REM Запустить приложение
echo ✅ Запуск API сервера...
echo.
echo 📚 Документация доступна: http://localhost:8000/docs
echo 🔌 API базовый URL: http://localhost:8000
echo.

python main.py

pause

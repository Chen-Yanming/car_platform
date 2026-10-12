@echo off
chcp 65001 >nul
echo ========================================
echo 启动后端服务
echo ========================================
echo.

cd /d "%~dp0"

if not exist .venv\Scripts\activate.bat (
    echo 错误：虚拟环境不存在，请先运行 setup_venv.bat
    pause
    exit /b 1
)

echo 激活虚拟环境...
call .venv\Scripts\activate.bat

echo 启动服务器...
uvicorn app.main:app --host 0.0.0.0 --port 9000 --reload


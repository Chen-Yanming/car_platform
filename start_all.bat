@echo off
chcp 65001 >nul
set "ROOT=%~dp0"

if not exist "%ROOT%backend\.venv\Scripts\activate.bat" (
    echo 首次启动：正在创建后端虚拟环境并安装依赖...
    call "%ROOT%backend\setup_venv.bat"
    if errorlevel 1 exit /b 1
)

start "Car Platform Backend" /D "%ROOT%backend" cmd /k start_server.bat
start "Car Platform Frontend" /D "%ROOT%frontend" cmd /k start_frontend.bat

echo.
echo 后端 API 文档：http://localhost:9000/docs
echo 前端页面：    http://localhost:8080
echo.
echo 首次安装依赖可能需要几分钟，请等待两个服务启动完成。
pause


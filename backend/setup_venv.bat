@echo off
chcp 65001 >nul
echo ========================================
echo 正在设置Windows虚拟环境
echo ========================================
echo.

cd /d "%~dp0"

echo [1/4] 删除旧的虚拟环境（如果存在）...
if exist .venv (
    echo 发现旧的虚拟环境，正在删除...
    rmdir /s /q .venv
    echo 已删除旧的虚拟环境
) else (
    echo 未找到旧的虚拟环境
)
echo.

echo [2/4] 创建新的虚拟环境...
python -m venv .venv
if errorlevel 1 (
    echo 错误：无法创建虚拟环境，请确保已安装Python
    pause
    exit /b 1
)
echo 虚拟环境创建成功
echo.

echo [3/4] 激活虚拟环境并安装依赖...
call .venv\Scripts\activate.bat
if errorlevel 1 (
    echo 错误：无法激活虚拟环境
    pause
    exit /b 1
)
echo 虚拟环境已激活
echo.

echo [4/4] 安装依赖包...
pip install -r requirements.txt
if errorlevel 1 (
    echo 错误：依赖安装失败
    pause
    exit /b 1
)
echo.
echo ========================================
echo 虚拟环境设置完成！
echo ========================================
echo.
echo 要启动后端服务，请运行：
echo   .venv\Scripts\activate.bat
echo   uvicorn app.main:app --host 0.0.0.0 --port 9000 --reload
echo.
pause


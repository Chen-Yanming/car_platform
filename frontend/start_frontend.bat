@echo off
chcp 65001 >nul
echo ========================================
echo 启动前端开发服务器
echo ========================================
echo.

cd /d "%~dp0"

if not exist node_modules (
    echo [1/3] 检测到未安装依赖，正在安装...
    call npm install
    if errorlevel 1 (
        echo 错误：依赖安装失败
        pause
        exit /b 1
    )
    echo 依赖安装完成
    echo.
) else (
    echo [1/3] 依赖已安装，跳过安装步骤
    echo.
)

if not exist .env (
    echo [2/3] 创建 .env 配置文件...
    copy env.example .env >nul
    echo 已从 env.example 创建 .env 文件
    echo 请检查 .env 文件中的 VITE_API_BASE 配置是否正确
    echo.
) else (
    echo [2/3] .env 文件已存在
    echo.
)

echo [3/3] 启动开发服务器...
echo.
echo 前端服务将在 http://localhost:8080 启动
echo 按 Ctrl+C 停止服务
echo ========================================
echo.

call npm run dev


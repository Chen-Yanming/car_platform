# Car Platform

车辆平台前后端项目，包含 Vue 3 + Vite 前端和 FastAPI 后端。默认使用模拟设备数据，适合本地启动和界面联调。

## 一键启动（Windows）

1. 安装 [Python 3.10 或更高版本](https://www.python.org/downloads/) 和 [Node.js LTS](https://nodejs.org/)（安装 Node.js 时会同时安装 npm）。
2. 在项目根目录双击 `start_all.bat`。
3. 首次启动时，脚本会在后端创建 Python 虚拟环境并安装依赖；前端启动脚本会自动安装 npm 依赖。首次安装需要联网。
4. 两个服务会分别在命令窗口运行。关闭对应窗口即可停止服务。

如果 Windows 阻止脚本运行，也可以在项目目录打开命令提示符并执行：

```bat
start_all.bat
```

## 访问地址

| 服务 | 地址 | 用途 |
| --- | --- | --- |
| 前端页面 | http://localhost:8080 | 操作界面 |
| 后端 API 文档 | http://localhost:9000/docs | Swagger API 文档 |
| 后端健康检查 | http://localhost:9000/health | 服务状态 |

前端开发服务器会把 `/api` 请求转发到 `http://localhost:9000`。如需单独启动，可分别运行 `backend\start_server.bat` 和 `frontend\start_frontend.bat`。

## 项目结构

```text
backend/    FastAPI 服务、设备通信与模拟数据
frontend/   Vue 3 + Vite 前端
start_all.bat  一键启动前后端
```

## 配置说明

后端配置模板位于 `backend/env.example`，前端配置模板位于 `frontend/env.example`。本地 `.env` 文件不会提交到 Git；首次运行前端脚本时会从模板生成 `frontend/.env`。后端默认启用模拟模式（`IOT_MOCK_MODE=true`）。接入实际设备前，请在本机 `backend/.env` 中配置网关地址、端口和设备参数，并按需关闭模拟模式。

## 常见问题

- **端口已被占用：** 关闭占用 8080 或 9000 端口的进程，或调整相应服务配置后重启。
- **依赖安装失败：** 确认 Python、Node.js 和 npm 已安装，并检查网络连接；之后重新运行对应目录的启动脚本。
- **无法连接设备：** 默认模拟模式不需要真实设备。实际设备联调时，检查 `backend/.env` 中的网关配置及本机网络连通性。

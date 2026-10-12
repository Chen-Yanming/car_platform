# 智能钻孔车触摸屏前端

本目录提供一个与现场触摸屏一致的 Vue 前端界面，覆盖主界面及回转、压紧、进给三个伺服参数画面，并通过 Vite 提供开发/构建能力。

## 环境准备

1. 安装 Node.js（建议 18+，最低 12.x 可运行 Vite 2）。
2. 进入 `frontend` 目录并安装依赖。

### Windows

**方式1：使用批处理脚本（推荐）**

直接双击运行 `start_frontend.bat`，脚本会自动：
- 检查并安装依赖（如果未安装）
- 创建 `.env` 配置文件（如果不存在）
- 启动开发服务器

**方式2：手动设置**

```powershell
cd "D:\platform project\car platform\frontend"

# 安装依赖
   npm install

# 创建环境配置文件
copy env.example .env

# 编辑 .env 文件，设置后端API地址
# VITE_API_BASE=http://localhost:9000

# 启动开发服务器
npm run dev
   ```

### Linux/macOS

```bash
cd /home/cym/platform/frontend
npm install
cp env.example .env          # 设置 VITE_API_BASE 指向后端
npm run dev -- --host 0.0.0.0 --port 8080
```

## 本地预览

启动后，浏览器访问 `http://localhost:8080`（Windows）或 `http://<服务器IP>:8080`（Linux/macOS）即可切换四个界面，并通过 `VITE_API_BASE` 与后端交互。

**重要**：确保后端服务已启动（默认端口 9000），并在 `.env` 文件中正确配置 `VITE_API_BASE`。

## 生产构建

### Windows

```powershell
cd "D:\platform project\car platform\frontend"
npm run build
npm run preview   # 本地预览打包结果
```

### Linux/macOS

```bash
npm run build
npm run preview   # 本地预览打包结果
```

## 结构

- `index.html`：Vite 入口文件，挂载 Vue 应用。
- `src/main.js`：应用入口，注册全局样式。
- `src/App.vue`：主界面，包含四个触摸屏画面和交互逻辑。
- `src/components/ServoPanel.vue`：伺服参数共用组件。
- `src/assets/styles.css`：界面样式，按触摸屏配色搭建布局。

如需接入实际 PLC 或上位机，可在 `src/App.vue` 中对接真实数据源或 WebSocket。


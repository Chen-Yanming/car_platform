## 智能钻孔车后端服务

该目录提供一个使用 FastAPI 编写的轻量后端，用于把前端触摸屏的操作映射到 PLC Modbus 寄存器。前端按钮通过 `POST /api/registers/write` 调用，把动作标识与目标值传给后端，后端再依据 `register_map.py` 中的映射信息通过 Modbus TCP 协议向 PLC 网关读写寄存器。

### 环境准备

#### Linux/macOS

```bash
cd /home/cym/platform/backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

#### Windows

**重要提示**：如果 `.venv` 文件夹是在 Linux/macOS 上创建的（包含 `bin` 文件夹），在 Windows 上无法直接使用。需要在 Windows 上重新创建虚拟环境。

**方式1：使用Python脚本（推荐，最简单）**

直接运行 `setup_and_run.py`，脚本会自动完成所有步骤并启动服务：

```bash
python setup_and_run.py
```

或者在文件资源管理器中双击 `setup_and_run.py` 文件。

脚本会自动：
- 删除旧的虚拟环境（如果存在）
- 创建新的Windows虚拟环境
- 升级pip
- 安装所有依赖包
- 启动后端服务

**方式2：使用批处理脚本**

直接双击运行 `setup_venv.bat`，脚本会自动：
- 删除旧的虚拟环境（如果存在）
- 创建新的Windows虚拟环境
- 安装所有依赖包

然后双击运行 `start_server.bat` 启动服务。

**方式2：手动设置**

**首次设置或重新创建虚拟环境**：

```powershell
cd "D:\platform project\car platform\backend"

# 如果已有Linux/macOS创建的虚拟环境，先删除（可选）
# Remove-Item -Recurse -Force .venv

# 在Windows上创建新的虚拟环境
python -m venv .venv
```

**激活虚拟环境并安装依赖**：

```powershell
# 方式1：使用点斜杠前缀（推荐）
.\venv\Scripts\Activate.ps1

# 方式2：如果方式1失败，使用调用操作符
& .venv\Scripts\Activate.ps1

# 方式3：如果PowerShell执行策略受限，使用批处理文件
.venv\Scripts\activate.bat

# 安装依赖
pip install -r requirements.txt
```

**注意**：如果 PowerShell 执行策略限制导致无法激活，请先运行：
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```
然后重新打开PowerShell窗口。

### 配置

复制 `env.example` 为 `.env` 并补充实际的物联网接口地址、凭证等信息：

```bash
cp env.example .env
```

关键变量：

- `IOT_MOCK_MODE`：为 `true` 时只在本地缓存寄存器值，便于调试；为 `false` 时连接真实 Modbus 网关。
- `GATEWAY_IP`：Modbus TCP 网关的 IP 地址（如 `192.168.3.88`）。
- `GATEWAY_PORT`：Modbus TCP 端口，默认 `502`。
- `MODBUS_UNIT_ID`：Modbus 站号/单元ID，默认 `1`（如果地址格式为 `1 M 40`，站号会从地址中提取）。
- `REQUEST_TIMEOUT`：请求超时时间（秒），默认 `5`。

寄存器映射位于 `app/register_map.py`。如 PLC 寄存器有调整，只需修改该文件即可，无需改动业务代码。

### 启动

#### Linux/macOS

```bash
cd /home/cym/platform/backend
source .venv/bin/activate
uvicorn app.main:app --host 0.0.0.0 --port 9000 --reload
```

#### Windows

**方式1：使用批处理脚本（推荐）**

直接双击运行 `start_server.bat`，脚本会自动激活虚拟环境并启动服务。

**方式2：PowerShell 手动启动**：

```powershell
cd "D:\platform project\car platform\backend"
.\venv\Scripts\Activate.ps1
uvicorn app.main:app --host 0.0.0.0 --port 9000 --reload
```

如果上述方式失败，可以尝试：
```powershell
& .venv\Scripts\Activate.ps1
uvicorn app.main:app --host 0.0.0.0 --port 9000 --reload
```

**方式3：CMD 批处理方式**（如果PowerShell有问题）：

```cmd
cd "D:\platform project\car platform\backend"
.venv\Scripts\activate.bat
uvicorn app.main:app --host 0.0.0.0 --port 9000 --reload
```

**验证虚拟环境已激活**：
激活成功后，命令提示符前会显示 `(.venv)`，例如：
```
(.venv) PS D:\platform project\car platform\backend>
```

前端可通过 `VITE_API_BASE=http://<服务器IP>:9000` 访问该服务。

### Windows 启动故障排除

**问题1：无法加载模块".venv" 或找不到 Scripts 文件夹**

如果看到 `无法加载模块".venv"` 或找不到 `Scripts` 文件夹，可能的原因：

1. **虚拟环境是在 Linux/macOS 上创建的**：
   - 检查是否有 `bin` 文件夹而不是 `Scripts` 文件夹
   - 如果是，需要删除旧虚拟环境并在 Windows 上重新创建：
   ```powershell
   Remove-Item -Recurse -Force .venv
   python -m venv .venv
   ```

2. **虚拟环境未正确创建**：
   - 检查虚拟环境是否存在：`Test-Path .venv`
   - 如果不存在，先创建：`python -m venv .venv`

3. **使用正确的激活命令**：
   - Windows PowerShell：`.\venv\Scripts\Activate.ps1`（注意 `.\` 前缀）
   - Windows CMD：`.venv\Scripts\activate.bat`

**问题2：PowerShell 执行策略限制**

如果提示脚本无法执行，运行：
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```
然后关闭并重新打开PowerShell窗口。

**问题3：uvicorn 命令未找到**

确保：
1. 虚拟环境已成功激活（提示符前有 `(.venv)`）
2. 已安装依赖：`pip install -r requirements.txt`
3. 如果仍失败，尝试：`python -m uvicorn app.main:app --host 0.0.0.0 --port 9000 --reload`

### 日志

每次成功写入寄存器都会记录在 `backend/logs/register.log`，包含动作标识、寄存器名称、地址、写入值以及当前是否处于 mock 模式。日志文件采用滚动方式，方便追溯前端操作。

### API 示例

```bash
curl -X POST http://127.0.0.1:9000/api/registers/write \
  -H "Content-Type: application/json" \
  -d '{"action":"core_drill_start","value":true}'
```

### 连接真实设备

1. **配置 `.env` 文件**：
   ```bash
   IOT_MOCK_MODE=false
   GATEWAY_IP=192.168.3.88    # 替换为实际的 Modbus 网关 IP
   GATEWAY_PORT=502
   MODBUS_UNIT_ID=1            # 根据实际 PLC 站号调整
   ```

2. **确认网络连通性**：
   确保后端服务器能够访问 Modbus 网关（同一网段或路由可达）。

3. **验证寄存器地址**：
   对照 `app/register_map.py` 中的地址格式与 PLC 实际寄存器分配表：
   - `1 M 40` → 站号1，线圈地址40
   - `D1895.2` → 保持寄存器1895，位2
   - `D1900` → 保持寄存器1900

4. **重启后端服务**：
   
   **Linux/macOS**:
   ```bash
   # 停止当前服务后重新启动
   uvicorn app.main:app --host 0.0.0.0 --port 9000
   ```
   
   **Windows**:
   ```powershell
   # 停止当前服务后重新启动
   uvicorn app.main:app --host 0.0.0.0 --port 9000
   ```

5. **查看日志**：
   操作前端按钮后，检查 `logs/register.log` 确认寄存器读写是否成功。

### 地址格式说明

- **线圈（M 寄存器）**：`1 M 40` → 站号1，线圈地址40
- **保持寄存器（D 寄存器）**：
  - `D1900` → 保持寄存器1900（16位整数或32位浮点数）
  - `D1895.2` → 保持寄存器1895的第2位（布尔值）
  - `1 D 100` → 站号1，保持寄存器100

若启用 mock 模式，响应会包含本地缓存的寄存器值。部署到生产时请将 `IOT_MOCK_MODE` 设为 `false` 并配置真实的 Modbus 网关参数。


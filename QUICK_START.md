# 🚀 TG Realtime Forward 快速开始

## 📦 文件说明

您下载的压缩包包含以下文件：

### 核心文件
- `TG_Realtime_Forward.py` - **主程序文件** (实时转发核心功能)
- `config.py` - **配置示例文件** (参考配置)
- `README.md` - **详细说明文档**

### 启动脚本
- `start_forward.sh` - **Linux/Mac启动脚本**
- `start_forward.bat` - **Windows启动脚本**

### 管理工具
- `manage_service.sh` - **服务管理脚本** (启动/停止/监控)
- `check_environment.py` - **环境检查脚本**
- `test_config.py` - **配置测试脚本**

### 文档文件
`README.md` - **完整使用文档**
`QUICK_START.md` - **快速部署指南**
`项目根目录文件说明` - **项目根目录文件说明**

## ⚡ 5分钟快速部署

### 1. 环境准备
```bash
# 安装依赖 (所有系统通用)
pip install telethon asyncio
```

### 2. 配置设置 (关键步骤)
```bash
# 编辑配置文件 (必须修改以下项目)
nano config.py  # Linux/Mac
# 或用文本编辑器打开 config.py (Windows)
```

**必须修改的配置项：**
```python
# 1. 账号配置 - 替换为您的API信息
ACCOUNTS = [
    {
        "api_id": 您的API_ID,      # 从 https://my.telegram.org 获取
        "api_hash": "您的API_HASH", # 从 https://my.telegram.org 获取
        "session_name": "forward_session_1",
        "enabled": True
    },
]

# 2. 频道配置 - 替换为您的频道信息
PRESET_SOURCE_CHANNELS = [
    -1001234567890,           # 源频道1的ID
    "@source_channel",        # 源频道2的用户名
]

PRESET_TARGET_CHANNEL = -1009876543210  # 目标频道ID
```

### 3. 启动服务

#### Linux/Mac
```bash
# 方法1: 使用启动脚本
./start_forward.sh

# 方法2: 使用服务管理
./manage_service.sh start

# 方法3: 直接运行
python3 TG_Realtime_Forward.py
```

#### Windows
```cmd
# 双击运行 start_forward.bat
# 或命令行运行
start_forward.bat
```

### 4. 首次验证
首次运行时会要求您验证Telegram账号：
1. 程序会显示验证码请求
2. 输入您的手机号码
3. 输入收到的验证码
4. 完成验证后程序会自动运行

## 🔧 常用管理命令

### 查看服务状态
```bash
./manage_service.sh status    # Linux/Mac
tasklist | findstr python     # Windows
```

### 查看实时日志
```bash
./manage_service.sh logs      # Linux/Mac
tail -f tg_realtime_forward.log # 通用
```

### 查看转发统计
```bash
./manage_service.sh stats     # Linux/Mac
grep "转发成功" tg_realtime_forward.log | wc -l  # 统计转发数量
```

### 停止服务
```bash
./manage_service.sh stop      # Linux/Mac
taskkill /f /im python.exe    # Windows
```

## 📋 配置获取指南

### 获取Telegram API密钥
1. 访问 https://my.telegram.org
2. 使用您的Telegram账号登录
3. 点击 "API development tools"
4. 创建新应用，获取 `api_id` 和 `api_hash`

### 获取频道ID
1. 在Telegram中转发一条消息给 @userinfobot
2. 机器人会返回频道的详细信息，包括ID
3. 频道ID格式：`-1001234567890`

## 🚨 常见问题

### 1. 程序无法启动
- ✅ 检查Python版本 (需要3.7+)
- ✅ 检查依赖是否安装 `pip install telethon asyncio`
- ✅ 检查配置文件是否正确
- ✅ 运行环境检查: `python3 check_environment.py`

### 2. 配置文件错误
- ✅ 运行配置测试: `python3 test_config.py`
- ✅ 检查API密钥是否正确
- ✅ 检查频道ID格式是否正确

### 3. 连接失败
- ✅ 检查网络连接
- ✅ 如需要代理，请在config.py中配置 `GLOBAL_PROXY`
- ✅ 检查防火墙设置

### 4. 转发失败
- ✅ 确认机器人有目标频道的写入权限
- ✅ 检查目标频道是否设置了限制
- ✅ 查看日志获取详细错误信息

## 🎯 功能特性

✅ **实时转发** - 只转发新消息，不处理历史消息  
✅ **7*24小时运行** - 自动重连，异常恢复  
✅ **智能过滤** - 广告过滤、内容质量过滤  
✅ **去重处理** - 避免转发重复内容  
✅ **多账号支持** - 账号轮换，避免限制  
✅ **完整日志** - 详细记录运行状态  

## 📞 技术支持

如果遇到问题：
1. 先运行 `python3 check_environment.py` 检查环境
2. 运行 `python3 test_config.py` 测试配置
3. 查看日志文件 `tg_realtime_forward.log`
4. 参考详细文档 `README.md`

## ⚡ 一键部署命令

```bash
# Linux/Mac 一键部署
cd /path/to/your/folder
pip install telethon asyncio
echo "请编辑 config.py 文件配置您的信息"
./start_forward.sh
```

```cmd
# REM Windows 一键部署
cd C:\path\to\your\folder
pip install telethon asyncio
copy config_example.py config.py
echo 请编辑 config.py 文件配置您的信息
start_forward.bat
```

---

**🎉 配置完成后，您的Telegram实时转发服务就可以开始工作了！**

**重要提醒**: 首次运行需要完成Telegram验证，请确保您能接收验证码。
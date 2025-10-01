# TG-Realtime-Forward
TG Realtime Forward 是一个基于 Python 的 Telegram 实时消息转发工具，它能够7*24小时不间断地监听源频道的新消息，并实时转发到目标频道。该工具保留了原始TG_ZF.py的所有高级功能，包括广告过滤、内容质量过滤、去重处理等。
# TG Realtime Forward - Telegram实时消息转发工具

## 📋 项目简介

TG Realtime Forward 是一个基于 Python 的 Telegram 实时消息转发工具，它能够7*24小时不间断地监听源频道的新消息，并实时转发到目标频道。该工具保留了原始TG_ZF.py的所有高级功能，包括广告过滤、内容质量过滤、去重处理等。

## ✨ 主要特性

- **🔄 实时转发**: 只转发启动后收到的新消息，不处理历史消息
- **⏰ 7*24小时运行**: 自动重连，异常恢复，持续稳定运行
- **🎯 智能过滤**: 广告检测、内容质量过滤、重复内容去重
- **👥 多账号支持**: 支持账号轮换，避免频繁操作限制
- **📊 完整日志**: 详细的运行日志和统计信息
- **🛡️ 错误处理**: 完善的错误处理和自动恢复机制

## 🚀 快速开始

### 1. 环境准备

#### 系统要求
- Python 3.7+
- 稳定的网络连接
- Telegram账号（需要API密钥）

#### 安装依赖
```bash
pip install telethon asyncio
```

#### 获取Telegram API密钥
1. 访问 https://my.telegram.org
2. 使用您的Telegram账号登录
3. 进入"API development tools"
4. 创建新的应用程序，获取 `api_id` 和 `api_hash`

### 2. 配置设置

#### 修改配置
编辑 `config.py` 文件，修改以下关键配置：

```python
# 账号配置
ACCOUNTS = [
    {
        "api_id": 您的API_ID,
        "api_hash": "您的API_HASH",
        "session_name": "forward_session_1",
        "enabled": True
    },
]

# 频道配置
PRESET_SOURCE_CHANNELS = [
    -1001234567890,  # 源频道1的ID
    "@channel_username",  # 源频道2的用户名
]

PRESET_TARGET_CHANNEL = -1009876543210  # 目标频道ID
```

### 3. 运行程序

#### 首次运行
首次运行时会要求您验证Telegram账号：
```bash
python TG_Realtime_Forward.py
```

按照提示输入验证码完成验证。

#### 后台运行（推荐）
```bash
# Linux/Mac
nohup python TG_Realtime_Forward.py > forward.log 2>&1 &

# Windows (使用PowerShell)
Start-Process python -ArgumentList "TG_Realtime_Forward.py" -RedirectStandardOutput "forward.log" -RedirectStandardError "error.log"
```

## 📖 详细配置说明

### 代理配置
如果您的网络需要代理才能访问Telegram，请配置代理：

```python
# SOCKS5代理
GLOBAL_PROXY = {
    "proxy_type": "socks5",
    "addr": "127.0.0.1",
    "port": 1080,
    "username": "",
    "password": ""
}

# HTTP代理
GLOBAL_PROXY = {
    "proxy_type": "http",
    "addr": "127.0.0.1",
    "port": 8080,
    "username": "",
    "password": ""
}
```

### 多账号配置
配置多个账号可以实现账号轮换，避免频繁操作限制：

```python
ACCOUNTS = [
    {
        "api_id": 11111111,
        "api_hash": "hash1",
        "session_name": "forward_session_1",
        "enabled": True
    },
    {
        "api_id": 22222222,
        "api_hash": "hash2", 
        "session_name": "forward_session_2",
        "enabled": True
    },
]
```

### 频道配置
支持多种频道标识格式：

```python
PRESET_SOURCE_CHANNELS = [
    -1001234567890,           # 频道ID
    "@channel_username",      # 频道用户名
    "https://t.me/channel",   # 频道链接
]
```

### 过滤配置
可以根据需求调整过滤规则：

```python
# 广告关键词
AD_KEYWORDS = [
    "推广", "广告", "营销", "代理", "加盟",
    # ... 添加您的关键词
]

# 内容质量过滤
ENABLE_CONTENT_FILTER = True
MEANINGLESS_WORDS = [
    "哈哈", "呵呵", "👍", "打卡",
    # ... 添加无意义词汇
]
```

## 🔧 高级功能

### 账号轮换
当转发消息数量达到 `ROTATION_INTERVAL` 设置值时，系统会自动切换到下一个账号：

```python
ENABLE_ACCOUNT_ROTATION = True
ROTATION_INTERVAL = 500  # 每500条消息轮换一次
ACCOUNT_DELAY = 5        # 切换延迟5秒
```

### 智能切换
启用智能账号切换后，系统会自动检测账号对频道的访问权限，跳过无法访问的账号：

```python
ENABLE_SMART_ACCOUNT_SWITCH = True
```

### 健康检查
系统会定期检查运行状态，确保服务稳定：

```python
HEALTH_CHECK_INTERVAL = 300  # 每5分钟检查一次
MAX_RECONNECT_ATTEMPTS = 10  # 最大重连尝试次数
RECONNECT_DELAY = 60         # 重连延迟60秒
```

## 📊 日志和监控

### 日志文件
程序会生成详细的运行日志：
- `tg_realtime_forward.log` - 主要运行日志
- `forward_history.json` - 转发历史记录
- `dedup_history.json` - 去重历史记录

### 监控运行状态
```bash
# 查看实时日志
tail -f tg_realtime_forward.log

# 查看转发统计
grep "转发成功" tg_realtime_forward.log | wc -l

# 查看错误信息
grep "ERROR" tg_realtime_forward.log
```

## 🛠️ 故障排除

### 常见问题

#### 1. 连接失败
**问题**: 无法连接到Telegram服务器
**解决**: 
- 检查网络连接
- 确认代理配置正确
- 验证API密钥是否正确

#### 2. 频繁触发限制
**问题**: 收到 "FloodWait" 错误
**解决**:
- 增加转发延迟 `DELAY_SINGLE` 和 `DELAY_GROUP`
- 启用多账号轮换
- 减少同时监听的源频道数量

#### 3. 消息转发失败
**问题**: 消息无法转发到目标频道
**解决**:
- 确认机器人有目标频道的写入权限
- 检查目标频道是否设置了限制
- 验证频道ID是否正确

#### 4. 程序异常退出
**问题**: 程序运行一段时间后崩溃
**解决**:
- 检查系统资源是否充足
- 查看日志文件了解具体错误
- 确保Python环境稳定

### 调试模式
启用详细日志记录：
```python
# 在TG_Realtime_Forward.py中修改日志级别
logging.basicConfig(
    level=logging.DEBUG,  # 改为DEBUG级别
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(Config.log_file, encoding='utf-8'),
        logging.StreamHandler()
    ]
)
```

## 🔒 安全建议

1. **保护API密钥**: 不要将API密钥泄露给他人
2. **限制权限**: 为转发机器人设置最小必要权限
3. **定期更新**: 及时更新依赖库和脚本
4. **监控日志**: 定期检查异常活动

## 📈 性能优化

### 减少资源占用
- 合理设置 `HEALTH_CHECK_INTERVAL`
- 适当调整转发延迟
- 使用多账号分散负载

### 提高转发效率
- 优化过滤规则，减少不必要的处理
- 使用SSD存储历史记录文件
- 确保网络连接稳定

## 📝 更新日志

### v1.0.0 (2024-01-01)
- ✅ 实时消息转发功能
- ✅ 7*24小时持续运行
- ✅ 多账号轮换支持
- ✅ 智能过滤系统
- ✅ 完善的错误处理
- ✅ 详细日志记录

## 🤝 贡献

欢迎提交Issue和Pull Request来改进这个项目！

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## ⚠️ 免责声明

本工具仅供学习和研究使用。使用者应遵守Telegram的服务条款，并承担使用本工具的所有责任。开发者不对因使用本工具造成的任何损失负责。

---

## 📞 联系方式

如有问题或建议，请通过以下方式联系：
- 提交 Issue
- 发送邮件

**祝您使用愉快！** 🎉

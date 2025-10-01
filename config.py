#!/usr/bin/env python3
"""
TG Realtime Forward 配置文件示例
根据您的需求进行修改
"""

# ============ 全局代理配置 ============
# 如果您的网络需要代理才能访问Telegram，请配置此项
# 支持 socks5, socks4, http, mtproto
# 设置为 None 表示不使用代理

# 无代理配置
GLOBAL_PROXY = None

# SOCKS5代理配置示例
# GLOBAL_PROXY = {
#     "proxy_type": "socks5",
#     "addr": "127.0.0.1",
#     "port": 1080,
#     "username": "",  # 可选，留空表示无需认证
#     "password": ""   # 可选，留空表示无需认证
# }

# HTTP代理配置示例
# GLOBAL_PROXY = {
#     "proxy_type": "http",
#     "addr": "127.0.0.1",
#     "port": 8080,
#     "username": "",
#     "password": ""
# }

# ============ 账号配置 ============
# 您可以配置多个Telegram账号以实现账号轮换
# 每个账号需要api_id, api_hash和session_name
# 获取方法：在 https://my.telegram.org 申请

ACCOUNTS = [
    {
        "api_id": 12345,  # 替换为您的API ID
        "api_hash": "12345",  # 替换为您的API Hash
        "session_name": "forward_session_1",  # session文件名
        "enabled": True  # 是否启用此账号
    },
    # 可以添加更多账号实现轮换
    # {
    #     "api_id": 您的第二个API_ID,
    #     "api_hash": "您的第二个API_HASH",
    #     "session_name": "forward_session_2",
    #     "enabled": True
    # },
]

# ============ 频道配置 ============
# 源频道配置 - 支持多种格式
# 1. 频道ID: -1001234567890
# 2. 频道用户名: "@channel_username" 
# 3. 频道链接: "https://t.me/channel_username"

PRESET_SOURCE_CHANNELS = [
    # 示例配置，请替换为您的实际源频道
    -1001670294604,  # 源频道1
]

# 目标频道配置 - 只支持单个目标频道
PRESET_TARGET_CHANNEL = -1001666667684  # 替换为您的目标频道ID

# ============ 实时转发配置 ============
# 是否启用实时转发（如果为False，脚本将不会启动）
ENABLE_REALTIME_FORWARD = True

# 是否只转发新消息（启动后收到的新消息）
FORWARD_ONLY_NEW_MESSAGES = True

# 异常重启延迟（秒）
AUTO_RESTART_DELAY = 30

# 健康检查间隔（秒）
HEALTH_CHECK_INTERVAL = 300

# 最大重连尝试次数
MAX_RECONNECT_ATTEMPTS = 10

# 重连延迟（秒）
RECONNECT_DELAY = 60

# ============ 账号轮换配置 ============
# 是否启用账号轮换
ENABLE_ACCOUNT_ROTATION = False

# 每转发多少条消息后轮换账号
ROTATION_INTERVAL = 500

# 账号切换延迟（秒）
ACCOUNT_DELAY = 5

# 是否启用智能账号切换（自动跳过无法访问频道的账号）
ENABLE_SMART_ACCOUNT_SWITCH = True

# ============ 转发延迟配置 ============
# 单条消息转发延迟（秒）
DELAY_SINGLE = 1

# 相册消息转发延迟（秒）
DELAY_GROUP = 4

# ============ 文件配置 ============
# 转发历史记录文件
FORWARD_HISTORY_FILE = "forward_history.json"

# 去重历史记录文件
DEDUP_HISTORY_FILE = "dedup_history.json"

# 日志文件
LOG_FILE = "tg_realtime_forward.log"

# ============ 广告过滤配置 ============
# 是否启用广告过滤
ENABLE_AD_FILTER = False

# 广告关键词列表
AD_KEYWORDS = [
    "广告",
    # 可以根据需要添加更多关键词
]

# 广告正则模式
AD_PATTERNS = [
   # r'https?://[^\s]+',  # 链接检测
   # r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',  # 邮箱检测
]

# 最小消息长度（小于此长度的消息可能被过滤）
MIN_MESSAGE_LENGTH = 1

# 每条消息最大链接数
MAX_LINKS_PER_MESSAGE = 13

# ============ 内容质量过滤配置 ============
# 是否启用内容质量过滤
ENABLE_CONTENT_FILTER = False

# 是否要求无意义消息必须有媒体内容
ENABLE_MEDIA_REQUIRED_FILTER = False

# 无意义词汇列表
MEANINGLESS_WORDS = [
    "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "Cy",
    "嗯", "哦", "啊", "额", "呃", "哈", "呵", "嘿", "嗨", "cy",
    "好的", "ok", "okay", "yes", "no", "是", "不是", "对", "不对",
    "哈哈", "呵呵", "嘿嘿", "嘻嘻", "嘿嘿嘿", "哈哈哈", "插眼",
    "顶", "赞", "👍", "👌", "😊", "😄", "😂", "😅",
    "沙发", "板凳", "地板", "地下室", "前排", "后排",
    "路过", "看看", "瞧瞧", "围观", "吃瓜", "打卡",
    "签到", "报到", "冒泡", "潜水", "灌水", "水贴"
]

# 最大重复字符数（如"哈哈哈"超过3个字符会被过滤）
MAX_REPEAT_CHARS = 13

# 最小有意义内容长度
MIN_MEANINGFUL_LENGTH = 1

# 最大表情符号比例（0.5表示50%）
MAX_EMOJI_RATIO = 1

# ============ 内容去重配置 ============
# 是否启用内容去重
ENABLE_CONTENT_DEDUPLICATION = True

# 目标频道扫描范围（条消息），None表示扫描所有
TARGET_CHANNEL_SCAN_LIMIT = None

# 是否显示详细的去重日志
VERBOSE_DEDUP_LOGGING = False

# ============ 高级配置 ============
# 批量进度显示间隔（条消息）
BATCH_PROGRESS_INTERVAL = 100

# 自动导出频道信息（设置为True时，程序启动时自动导出频道信息）
AUTO_EXPORT_CHANNELS = False

# ============ 配置验证 ============
def validate_config():
    """验证配置是否正确"""
    errors = []
    
    # 检查账号配置
    if not ACCOUNTS:
        errors.append("未配置任何账号")
    
    for i, account in enumerate(ACCOUNTS):
        if not account.get("api_id") or not account.get("api_hash"):
            errors.append(f"账号 {i+1} 缺少 api_id 或 api_hash")
        if not account.get("session_name"):
            errors.append(f"账号 {i+1} 缺少 session_name")
    
    # 检查频道配置
    if not PRESET_SOURCE_CHANNELS:
        errors.append("未配置源频道")
    
    if not PRESET_TARGET_CHANNEL:
        errors.append("未配置目标频道")
    
    # 检查数值配置
    if ROTATION_INTERVAL <= 0:
        errors.append("ROTATION_INTERVAL 必须大于0")
    
    if DELAY_SINGLE < 0 or DELAY_GROUP < 0:
        errors.append("延迟配置不能为负数")
    
    return errors

# ============ 配置导出函数 ============
def export_config_template():
    """导出配置模板"""
    config_template = {
        "global_proxy": GLOBAL_PROXY,
        "accounts": ACCOUNTS,
        "source_channels": PRESET_SOURCE_CHANNELS,
        "target_channel": PRESET_TARGET_CHANNEL,
        "realtime_config": {
            "enable_realtime_forward": ENABLE_REALTIME_FORWARD,
            "forward_only_new_messages": FORWARD_ONLY_NEW_MESSAGES,
            "auto_restart_delay": AUTO_RESTART_DELAY,
            "health_check_interval": HEALTH_CHECK_INTERVAL,
            "max_reconnect_attempts": MAX_RECONNECT_ATTEMPTS,
            "reconnect_delay": RECONNECT_DELAY
        },
        "account_rotation": {
            "enable_account_rotation": ENABLE_ACCOUNT_ROTATION,
            "rotation_interval": ROTATION_INTERVAL,
            "account_delay": ACCOUNT_DELAY,
            "enable_smart_account_switch": ENABLE_SMART_ACCOUNT_SWITCH
        },
        "delays": {
            "delay_single": DELAY_SINGLE,
            "delay_group": DELAY_GROUP
        },
        "files": {
            "forward_history_file": FORWARD_HISTORY_FILE,
            "dedup_history_file": DEDUP_HISTORY_FILE,
            "log_file": LOG_FILE
        },
        "filter_config": {
            "enable_ad_filter": ENABLE_AD_FILTER,
            "enable_content_filter": ENABLE_CONTENT_FILTER,
            "enable_media_required_filter": ENABLE_MEDIA_REQUIRED_FILTER,
            "enable_content_deduplication": ENABLE_CONTENT_DEDUPLICATION
        }
    }
    
    return config_template

if __name__ == "__main__":
    # 验证配置
    errors = validate_config()
    if errors:
        print("❌ 配置验证失败:")
        for error in errors:
            print(f"  - {error}")
        exit(1)
    
    print("✅ 配置验证通过")
    
    # 导出配置模板
    template = export_config_template()
    with open("current_config.json", "w", encoding="utf-8") as f:
        json.dump(template, f, indent=2, ensure_ascii=False)
    
    print("📋 当前配置已导出到 current_config.json")
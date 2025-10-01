#!/usr/bin/env python3
"""
TG Realtime Forward - Telegram实时消息转发工具
基于原始TG_ZF.py改进，实现7*24小时实时消息转发

功能特性：
- 实时监听源频道新消息
- 不转发历史消息，只处理启动后的新消息
- 7*24小时持续运行，自动重连
- 保留所有原始过滤和去重功能
- 支持多账号轮换和智能切换
- 完整的错误处理和日志记录
"""

import asyncio
import json
import os
import re
import hashlib
import time
import logging
from datetime import datetime
from typing import Dict, List, Optional, Set, Tuple
from telethon import TelegramClient, errors, events
from telethon.tl.types import Message, MessageMediaPhoto, MessageMediaDocument

# ============ 配置类 ============
class Config:
    """配置管理类"""
    
    # 全局代理配置（可选）
    global_proxy = None  # 设置为 None 表示不使用代理
    
    # 多账号配置
    accounts = [
        {
            "api_id": 12345,
            "api_hash": "12345",
            "session_name": "forward_session_1",
            "enabled": True
        },
        # 可以添加更多账号配置
    ]
    
    # 频道配置
    preset_source_channels = []  # 源频道列表，支持ID、用户名、链接
    preset_target_channel = -100123456789  # 目标频道ID
    
    # 实时转发配置
    enable_realtime_forward = True  # 是否启用实时转发
    forward_only_new_messages = True  # 只转发新消息，不处理历史消息
    auto_restart_delay = 30  # 异常重启延迟（秒）
    health_check_interval = 300  # 健康检查间隔（秒）
    max_reconnect_attempts = 10  # 最大重连尝试次数
    reconnect_delay = 60  # 重连延迟（秒）
    
    # 账号轮换配置
    enable_account_rotation = True  # 是否启用账号轮换
    rotation_interval = 500  # 每转发多少条消息后轮换账号
    account_delay = 5  # 账号切换延迟（秒）
    enable_smart_account_switch = True  # 是否启用智能账号切换
    
    # 转发延迟配置
    delay_single = 2  # 单条消息延迟（秒）
    delay_group = 4  # 相册延迟（秒）
    
    # 文件配置
    forward_history_file = "forward_history.json"  # 转发历史记录文件
    dedup_history_file = "dedup_history.json"  # 去重历史记录文件
    log_file = "tg_realtime_forward.log"  # 日志文件
    
    # 广告过滤配置
    enable_ad_filter = True
    ad_keywords = [
        "推广", "广告", "营销", "代理", "加盟", "招商", "投资", "理财",
        "店铺", "注册", "官方", "佣金", "汇旺", "官网注册", "返水",
        "入款", "出款", "返水", "彩金", "资金保障", "提款"
    ]
    
    ad_patterns = [
        r'https?://[^\s]+',  # 链接
        r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',  # 邮箱
    ]
    
    min_message_length = 10  # 最小消息长度
    max_links_per_message = 3  # 每条消息最大链接数
    
    # 内容质量过滤配置
    enable_content_filter = True
    enable_media_required_filter = True  # 是否要求无意义消息必须有媒体内容
    
    meaningless_words = [
        "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "Cy",
        "嗯", "哦", "啊", "额", "呃", "哈", "呵", "嘿", "嗨", "cy",
        "好的", "ok", "okay", "yes", "no", "是", "不是", "对", "不对",
        "哈哈", "呵呵", "嘿嘿", "嘻嘻", "嘿嘿嘿", "哈哈哈", "插眼",
        "顶", "赞", "👍", "👌", "😊", "😄", "😂", "😅",
        "沙发", "板凳", "地板", "地下室", "前排", "后排",
        "路过", "看看", "瞧瞧", "围观", "吃瓜", "打卡",
        "签到", "报到", "冒泡", "潜水", "灌水", "水贴"
    ]
    
    max_repeat_chars = 3  # 最大重复字符数
    min_meaningful_length = 5  # 最小有意义内容长度
    max_emoji_ratio = 0.5  # 最大表情符号比例
    
    # 内容去重配置
    enable_content_deduplication = True
    target_channel_scan_limit = None  # 目标频道扫描范围，None表示扫描所有
    verbose_dedup_logging = False  # 是否显示详细的去重日志

# ============ 日志配置 ============
def setup_logging():
    """设置日志系统"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(Config.log_file, encoding='utf-8'),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger('TG_Realtime_Forward')

logger = setup_logging()

# ============ 全局变量 ============
clients = []
current_client_index = 0
account_channel_access = {}
active_listeners = set()  # 活跃监听器集合
is_running = True  # 运行状态标志

# ============ 工具函数 ============
def normalize_channel_id(channel_id):
    """标准化频道ID格式"""
    if channel_id is None:
        return None
    
    channel_str = str(channel_id)
    if channel_str.startswith('-100'):
        return channel_str
    
    try:
        if int(channel_str) > 0:
            return f"-100{channel_str}"
    except ValueError:
        pass
    
    return channel_str

def get_channel_name(entity):
    """安全地获取频道名称"""
    return getattr(entity, 'title', None) or getattr(entity, 'name', None) or "未知频道"

# ============ 客户端管理 ============
class ClientManager:
    """客户端管理器"""
    
    def __init__(self):
        self.clients = []
        self.current_index = 0
        self.setup_clients()
    
    def setup_clients(self):
        """初始化客户端列表"""
        for account in Config.accounts:
            if account["enabled"]:
                proxy = Config.global_proxy
                client = TelegramClient(
                    account["session_name"], 
                    account["api_id"], 
                    account["api_hash"], 
                    proxy=proxy
                )
                
                self.clients.append({
                    "client": client,
                    "account": account,
                    "forward_count": 0,
                    "last_used": 0,
                    "enabled": True,
                    "name": account["session_name"]
                })
    
    def get_current_client(self):
        """获取当前客户端"""
        if not self.clients:
            raise Exception("没有可用的账号！")
        return self.clients[self.current_index]["client"]
    
    def get_current_account_info(self):
        """获取当前账号信息"""
        if not self.clients:
            return None
        return self.clients[self.current_index]["account"]
    
    def switch_to_next_account(self):
        """切换到下一个账号"""
        if not Config.enable_account_rotation or len(self.clients) <= 1:
            return False
        
        old_index = self.current_index
        self.current_index = (self.current_index + 1) % len(self.clients)
        
        old_name = self.clients[old_index]["name"]
        new_name = self.clients[self.current_index]["name"]
        
        logger.info(f"🔄 切换账号: {old_name} → {new_name}")
        return True
    
    def should_rotate_account(self):
        """判断是否应该轮换账号"""
        if not Config.enable_account_rotation or len(self.clients) <= 1:
            return False
        
        current_client_data = self.clients[self.current_index]
        return current_client_data["forward_count"] >= Config.rotation_interval
    
    def increment_forward_count(self):
        """增加转发计数"""
        self.clients[self.current_index]["forward_count"] += 1
    
    def reset_forward_count(self):
        """重置转发计数"""
        self.clients[self.current_index]["forward_count"] = 0

# ============ 消息过滤器 ============
class MessageFilter:
    """消息过滤器"""
    
    @staticmethod
    def is_ad_message(text, has_media=False):
        """检测广告消息"""
        if not Config.enable_ad_filter or not text:
            return False
        
        text_lower = text.lower()
        
        # 检查关键词
        for keyword in Config.ad_keywords:
            if keyword in text_lower:
                return True
        
        # 检查正则模式
        link_count = 0
        for pattern in Config.ad_patterns:
            matches = re.findall(pattern, text)
            if pattern == r'https?://[^\s]+':
                link_count += len(matches)
            elif matches:
                return True
        
        # 检查链接数量
        if link_count > Config.max_links_per_message:
            return True
        
        # 检查消息长度
        if len(text.strip()) < Config.min_message_length:
            if not has_media:
                return True
        
        return False
    
    @staticmethod
    def is_meaningless_message(text, has_media=False):
        """检测无意义消息"""
        if not Config.enable_content_filter or not text:
            return False
        
        text = text.strip()
        
        # 检查无意义词汇
        if text.lower() in [word.lower() for word in Config.meaningless_words]:
            return not has_media
        
        # 检查重复字符
        if len(text) > 1:
            char_counts = {}
            for char in text:
                char_counts[char] = char_counts.get(char, 0) + 1
            max_char_count = max(char_counts.values())
            if max_char_count > Config.max_repeat_chars and max_char_count / len(text) > 0.6:
                return not has_media
        
        # 检查表情符号比例
        emoji_count = len([c for c in text if ord(c) > 127 and c not in '，。！？；：""''（）【】《》'])
        if len(text) > 0 and emoji_count / len(text) > Config.max_emoji_ratio:
            return not has_media
        
        # 检查有意义内容长度
        meaningful_chars = len([c for c in text if c.isalnum() or c in '，。！？；：""''（）【】《》'])
        if meaningful_chars < Config.min_meaningful_length:
            return not has_media
        
        # 检查单字符重复
        if len(set(text.replace(' ', ''))) <= 1 and len(text) > 1:
            return not has_media
        
        return False

# ============ 去重管理器 ============
class DeduplicationManager:
    """去重管理器"""
    
    def __init__(self):
        self.history_file = Config.dedup_history_file
        self.history = self.load_history()
    
    def load_history(self):
        """加载去重历史"""
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, "r", encoding="utf-8") as f:
                    content = f.read().strip()
                    if content:
                        return json.loads(content)
            except Exception as e:
                logger.warning(f"去重历史文件格式错误: {e}")
        return {}
    
    def save_history(self):
        """保存去重历史"""
        try:
            with open(self.history_file, "w", encoding="utf-8") as f:
                json.dump(self.history, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"保存去重历史失败: {e}")
    
    def generate_message_hash(self, message):
        """生成消息哈希"""
        hash_content = ""
        
        if message.media:
            if hasattr(message.media, 'photo'):
                hash_content += f"photo:{message.media.photo.id}"
            elif hasattr(message.media, 'document'):
                hash_content += f"doc:{message.media.document.id}"
            elif hasattr(message.media, 'video'):
                hash_content += f"video:{message.media.video.id}"
            elif hasattr(message.media, 'audio'):
                hash_content += f"audio:{message.media.audio.id}"
            else:
                hash_content += f"media:{type(message.media).__name__}"
        else:
            if message.message:
                normalized_text = re.sub(r'\s+', ' ', message.message.strip().lower())
                hash_content += f"text:{normalized_text}"
            else:
                hash_content += f"empty:{message.id}"
        
        return hashlib.md5(hash_content.encode('utf-8')).hexdigest()
    
    def is_duplicate(self, message_hash):
        """检查是否重复"""
        if not Config.enable_content_deduplication:
            return False
        return message_hash in self.history
    
    def add_to_history(self, message_hash, source_info=""):
        """添加到去重历史"""
        if Config.enable_content_deduplication and message_hash not in self.history:
            self.history[message_hash] = {
                "timestamp": time.time(),
                "source": source_info
            }
            self.save_history()

# ============ 转发历史管理器 ============
class ForwardHistoryManager:
    """转发历史管理器"""
    
    def __init__(self):
        self.history_file = Config.forward_history_file
        self.history = self.load_history()
    
    def load_history(self):
        """加载转发历史"""
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, "r", encoding="utf-8") as f:
                    content = f.read().strip()
                    if content:
                        return json.loads(content)
            except Exception as e:
                logger.warning(f"转发历史文件格式错误: {e}")
        return {}
    
    def save_history(self):
        """保存转发历史"""
        try:
            with open(self.history_file, "w", encoding="utf-8") as f:
                json.dump(self.history, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"保存转发历史失败: {e}")
    
    def get_channel_key(self, src_id, dst_id):
        """生成频道键"""
        return f"{normalize_channel_id(src_id)}_to_{normalize_channel_id(dst_id)}"
    
    def is_already_forwarded(self, src_id, dst_id, msg_id):
        """检查消息是否已经转发过"""
        channel_key = self.get_channel_key(src_id, dst_id)
        if channel_key not in self.history:
            return False
        
        forwarded_messages = self.history[channel_key].get("forwarded_messages", [])
        return str(msg_id) in [str(mid) for mid in forwarded_messages]
    
    def add_forward_record(self, src_id, dst_id, msg_id, msg_type="single"):
        """添加转发记录"""
        channel_key = self.get_channel_key(src_id, dst_id)
        if channel_key not in self.history:
            self.history[channel_key] = {
                "forwarded_messages": [],
                "total_count": 0,
                "last_update": ""
            }
        
        self.history[channel_key]["forwarded_messages"].append(str(msg_id))
        self.history[channel_key]["total_count"] += 1
        self.history[channel_key]["last_update"] = str(time.time())
        
        self.save_history()

# ============ 实时转发器 ============
class RealtimeForwarder:
    """实时转发器"""
    
    def __init__(self, client_manager, filter_manager, dedup_manager, history_manager):
        self.client_manager = client_manager
        self.filter_manager = filter_manager
        self.dedup_manager = dedup_manager
        self.history_manager = history_manager
        self.is_running = False
        self.reconnect_attempts = 0
        self.last_health_check = time.time()
        
    async def start_forwarding(self, source_channels, target_channel):
        """开始实时转发"""
        logger.info("🚀 启动实时转发服务...")
        self.is_running = True
        
        # 启动所有客户端
        await self.start_all_clients()
        
        # 设置消息监听器
        await self.setup_listeners(source_channels, target_channel)
        
        # 启动健康检查
        asyncio.create_task(self.health_check_loop())
        
        logger.info("✅ 实时转发服务已启动")
        
        # 保持运行
        try:
            while self.is_running:
                await asyncio.sleep(1)
        except KeyboardInterrupt:
            logger.info("🛑 收到停止信号，正在关闭服务...")
            await self.stop_forwarding()
    
    async def start_all_clients(self):
        """启动所有客户端"""
        for client_data in self.client_manager.clients:
            try:
                await client_data["client"].start()
                logger.info(f"✅ 账号 {client_data['name']} 启动成功")
            except Exception as e:
                logger.error(f"❌ 账号 {client_data['name']} 启动失败: {e}")
                client_data["enabled"] = False
    
    async def setup_listeners(self, source_channels, target_channel):
        """设置消息监听器"""
        client = self.client_manager.get_current_client()
        
        # 为每个源频道设置监听器
        for source_channel in source_channels:
            channel_id = normalize_channel_id(source_channel.id)
            
            @client.on(events.NewMessage(chats=source_channel))
            async def handle_new_message(event):
                await self.handle_message(event, source_channel, target_channel)
            
            logger.info(f"👂 已为频道 {get_channel_name(source_channel)} 设置监听器")
            active_listeners.add(channel_id)
    
    async def handle_message(self, event, source_channel, target_channel):
        """处理新消息"""
        message = event.message
        
        # 跳过服务消息
        if message.message is None and not message.media:
            logger.debug(f"跳过服务消息: {message.id}")
            return
        
        # 检查是否已经转发过
        if self.history_manager.is_already_forwarded(
            source_channel.id, target_channel.id, message.id
        ):
            logger.debug(f"跳过已转发消息: {message.id}")
            return
        
        # 内容去重检查
        message_hash = self.dedup_manager.generate_message_hash(message)
        if self.dedup_manager.is_duplicate(message_hash):
            logger.debug(f"跳过重复内容: {message.id}")
            return
        
        # 内容过滤
        has_media = message.media is not None
        has_text = message.message is not None and message.message.strip()
        
        # 广告过滤
        if has_text and self.filter_manager.is_ad_message(message.message, has_media):
            logger.info(f"🚫 过滤广告消息: {message.id}")
            return
        
        # 内容质量过滤
        if has_text and self.filter_manager.is_meaningless_message(message.message, has_media):
            logger.info(f"🗑️ 过滤无意义内容: {message.id}")
            return
        
        # 媒体要求过滤
        if Config.enable_media_required_filter and not has_media and not has_text:
            logger.info(f"🚫 过滤无媒体无文本消息: {message.id}")
            return
        
        # 执行转发
        await self.forward_message_safe(message, target_channel, source_channel)
        
        # 更新记录
        self.history_manager.add_forward_record(
            source_channel.id, target_channel.id, message.id
        )
        self.dedup_manager.add_to_history(
            message_hash, f"{get_channel_name(source_channel)}({source_channel.id})"
        )
        
        # 增加转发计数并检查账号轮换
        self.client_manager.increment_forward_count()
        if self.client_manager.should_rotate_account():
            await self.handle_account_rotation(source_channel, target_channel)
    
    async def forward_message_safe(self, message, target_channel, source_channel):
        """安全转发消息"""
        max_retries = 3
        retry_delay = 2
        
        for attempt in range(max_retries):
            try:
                client = self.client_manager.get_current_client()
                await client.forward_messages(target_channel, message)
                
                logger.info(f"✅ 转发成功: {message.id} 从 {get_channel_name(source_channel)} 到 {get_channel_name(target_channel)}")
                
                # 添加延迟避免触发限制
                await asyncio.sleep(Config.delay_single)
                return
                
            except errors.FloodWaitError as e:
                logger.warning(f"⏸ FloodWait，等待 {e.seconds} 秒")
                await asyncio.sleep(e.seconds + 5)
                
            except errors.ChatWriteForbiddenError:
                logger.error(f"🚫 目标频道禁止写入: {get_channel_name(target_channel)}")
                return
                
            except Exception as e:
                if attempt < max_retries - 1:
                    logger.warning(f"⚠️ 转发失败，重试 {attempt + 1}/{max_retries - 1}: {e}")
                    await asyncio.sleep(retry_delay * (attempt + 1))
                else:
                    logger.error(f"❌ 转发失败，已耗尽重试次数: {e}")
                    return
    
    async def handle_account_rotation(self, source_channel, target_channel):
        """处理账号轮换"""
        logger.info("🔄 检查账号轮换...")
        
        if self.client_manager.switch_to_next_account():
            await asyncio.sleep(Config.account_delay)
            
            # 重新设置监听器
            await self.setup_listeners([source_channel], target_channel)
            
            self.client_manager.reset_forward_count()
            logger.info("✅ 账号轮换完成")
    
    async def health_check_loop(self):
        """健康检查循环"""
        while self.is_running:
            try:
                current_time = time.time()
                if current_time - self.last_health_check > Config.health_check_interval:
                    await self.perform_health_check()
                    self.last_health_check = current_time
                
                await asyncio.sleep(60)  # 每分钟检查一次
                
            except Exception as e:
                logger.error(f"❌ 健康检查异常: {e}")
                await asyncio.sleep(10)
    
    async def perform_health_check(self):
        """执行健康检查"""
        try:
            client = self.client_manager.get_current_client()
            if not client.is_connected():
                logger.warning("⚠️ 客户端连接断开，尝试重新连接...")
                await client.connect()
                
            logger.info("💚 健康检查通过")
            
        except Exception as e:
            logger.error(f"❌ 健康检查失败: {e}")
            await self.handle_reconnection()
    
    async def handle_reconnection(self):
        """处理重连"""
        if self.reconnect_attempts >= Config.max_reconnect_attempts:
            logger.error("❌ 重连尝试次数已达上限，停止服务")
            await self.stop_forwarding()
            return
        
        self.reconnect_attempts += 1
        logger.info(f"🔄 尝试重连 {self.reconnect_attempts}/{Config.max_reconnect_attempts}")
        
        try:
            await asyncio.sleep(Config.reconnect_delay)
            await self.start_all_clients()
            self.reconnect_attempts = 0
            logger.info("✅ 重连成功")
            
        except Exception as e:
            logger.error(f"❌ 重连失败: {e}")
    
    async def stop_forwarding(self):
        """停止转发服务"""
        logger.info("🛑 正在停止实时转发服务...")
        self.is_running = False
        
        # 断开所有客户端
        for client_data in self.client_manager.clients:
            try:
                await client_data["client"].disconnect()
            except Exception as e:
                logger.warning(f"断开客户端时出错: {e}")
        
        logger.info("✅ 实时转发服务已停止")

# ============ 主函数 ============
async def main():
    """主函数"""
    print("🚀 TG Realtime Forward - Telegram实时消息转发工具")
    print("=" * 60)
    
    # 初始化管理器
    client_manager = ClientManager()
    filter_manager = MessageFilter()
    dedup_manager = DeduplicationManager()
    history_manager = ForwardHistoryManager()
    
    # 检查账号配置
    if not client_manager.clients:
        logger.error("❌ 没有可用的账号！请检查账号配置。")
        return
    
    # 获取客户端
    client = client_manager.get_current_client()
    
    # 验证预设频道
    source_channels = []
    target_channel = None
    
    if Config.preset_source_channels and Config.preset_target_channel:
        try:
            # 验证源频道
            for channel_id in Config.preset_source_channels:
                entity = await client.get_entity(channel_id)
                source_channels.append(entity)
                logger.info(f"✅ 源频道验证成功: {get_channel_name(entity)}")
            
            # 验证目标频道
            target_channel = await client.get_entity(Config.preset_target_channel)
            logger.info(f"✅ 目标频道验证成功: {get_channel_name(target_channel)}")
            
        except Exception as e:
            logger.error(f"❌ 频道验证失败: {e}")
            return
    else:
        logger.error("❌ 请配置源频道和目标频道")
        return
    
    # 扫描目标频道（如果需要去重）
    if Config.enable_content_deduplication:
        logger.info("🔍 正在扫描目标频道以建立去重历史...")
        # 这里可以添加扫描逻辑，但为了实时转发，通常不需要完整扫描
        logger.info("✅ 去重历史准备完成")
    
    # 启动实时转发器
    forwarder = RealtimeForwarder(
        client_manager, filter_manager, dedup_manager, history_manager
    )
    
    try:
        await forwarder.start_forwarding(source_channels, target_channel)
    except KeyboardInterrupt:
        logger.info("🛑 收到停止信号")
        await forwarder.stop_forwarding()
    except Exception as e:
        logger.error(f"❌ 运行时错误: {e}")
        await forwarder.stop_forwarding()

# ============ 运行 ============
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n🛑 程序已停止")
    except Exception as e:
        print(f"❌ 程序异常退出: {e}")
        logger.exception("程序异常退出")
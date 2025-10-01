#!/usr/bin/env python3
"""
TG Realtime Forward 环境检查脚本
用于检查运行环境是否满足要求
"""

import sys
import os
import platform
import subprocess
import importlib
import json
from pathlib import Path

def check_python_version():
    """检查Python版本"""
    print("🔍 检查Python版本...")
    version = sys.version_info
    print(f"   Python版本: {version.major}.{version.minor}.{version.micro}")
    
    if version.major >= 3 and version.minor >= 7:
        print("   ✅ Python版本符合要求 (3.7+)")
        return True
    else:
        print("   ❌ Python版本过低，需要3.7或更高版本")
        return False

def check_dependencies():
    """检查依赖库"""
    print("\n🔍 检查依赖库...")
    
    required_packages = [
        ("telethon", "Telethon库"),
        ("asyncio", "AsyncIO库"),
    ]
    
    all_good = True
    
    for package, description in required_packages:
        try:
            module = importlib.import_module(package)
            version = getattr(module, "__version__", "未知版本")
            print(f"   ✅ {description}: {version}")
        except ImportError:
            print(f"   ❌ {description}: 未安装")
            all_good = False
    
    return all_good

def check_system_info():
    """检查系统信息"""
    print("\n🔍 检查系统信息...")
    print(f"   操作系统: {platform.system()} {platform.release()}")
    print(f"   架构: {platform.machine()}")
    print(f"   Python路径: {sys.executable}")
    
    # 检查网络连接
    print("\n🔍 检查网络连接...")
    try:
        import socket
        # 测试连接到Telegram服务器
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        result = sock.connect_ex(('149.154.167.50', 443))  # Telegram服务器IP
        sock.close()
        
        if result == 0:
            print("   ✅ 可以连接到Telegram服务器")
        else:
            print("   ⚠️  可能无法连接到Telegram服务器，请检查网络")
    except Exception as e:
        print(f"   ⚠️  网络检查失败: {e}")

def check_files():
    """检查必要文件"""
    print("\n🔍 检查必要文件...")
    
    required_files = [
        ("TG_Realtime_Forward.py", "主程序文件"),
        ("config_example.py", "配置示例文件"),
        ("README.md", "说明文档"),
    ]
    
    for filename, description in required_files:
        if os.path.exists(filename):
            size = os.path.getsize(filename)
            print(f"   ✅ {description}: {filename} ({size} bytes)")
        else:
            print(f"   ❌ {description}: {filename} (缺失)")
    
    # 检查配置文件
    if os.path.exists("config.py"):
        print("   ✅ 配置文件: config.py (已存在)")
        return True
    else:
        print("   ⚠️  配置文件: config.py (未找到，需要创建)")
        return False

def check_config():
    """检查配置文件内容"""
    if not os.path.exists("config.py"):
        return False
    
    print("\n🔍 检查配置文件内容...")
    
    try:
        # 动态导入配置
        sys.path.insert(0, os.getcwd())
        import config
        
        checks = [
            ("ACCOUNTS", "账号配置"),
            ("PRESET_SOURCE_CHANNELS", "源频道配置"),
            ("PRESET_TARGET_CHANNEL", "目标频道配置"),
        ]
        
        all_good = True
        for attr, description in checks:
            if hasattr(config, attr):
                value = getattr(config, attr)
                if value:
                    if isinstance(value, list):
                        print(f"   ✅ {description}: {len(value)} 个配置项")
                    else:
                        print(f"   ✅ {description}: 已配置")
                else:
                    print(f"   ❌ {description}: 未配置")
                    all_good = False
            else:
                print(f"   ❌ {description}: 缺少配置项")
                all_good = False
        
        return all_good
        
    except Exception as e:
        print(f"   ❌ 配置文件检查失败: {e}")
        return False

def check_disk_space():
    """检查磁盘空间"""
    print("\n🔍 检查磁盘空间...")
    
    try:
        if platform.system() == "Windows":
            import shutil
            total, used, free = shutil.disk_usage("C:\\")
        else:
            stat = os.statvfs(".")
            total = stat.f_blocks * stat.f_frsize
            free = stat.f_bavail * stat.f_frsize
        
        free_gb = free / (1024**3)
        print(f"   可用空间: {free_gb:.2f} GB")
        
        if free_gb > 1:
            print("   ✅ 磁盘空间充足")
            return True
        else:
            print("   ⚠️  磁盘空间可能不足")
            return False
            
    except Exception as e:
        print(f"   ⚠️  磁盘空间检查失败: {e}")
        return True  # 不阻止运行

def generate_report():
    """生成检查报告"""
    print("\n" + "="*60)
    print("📊 环境检查报告")
    print("="*60)
    
    results = {
        "python_version": check_python_version(),
        "dependencies": check_dependencies(),
        "files": check_files(),
        "config": check_config(),
        "disk_space": check_disk_space(),
    }
    
    check_system_info()
    
    print("\n📋 检查结果汇总:")
    print("-" * 30)
    
    all_passed = True
    for check, result in results.items():
        status = "✅ 通过" if result else "❌ 失败"
        print(f"   {check}: {status}")
        if not result:
            all_passed = False
    
    print("\n" + "="*60)
    
    if all_passed:
        print("🎉 所有检查通过！环境已准备就绪")
        print("\n下一步:")
        print("   1. 运行 ./start_forward.sh (Linux/Mac) 或 start_forward.bat (Windows)")
        print("   2. 按照提示完成首次验证")
        print("   3. 开始享受实时转发服务！")
    else:
        print("⚠️  环境检查未完全通过")
        print("\n请解决上述问题后再运行程序")
        
        if not results["config"]:
            print("\n💡 配置建议:")
            print("   1. 复制 config_example.py 为 config.py")
            print("   2. 编辑 config.py 文件")
            print("   3. 配置您的API密钥和频道信息")
        
        if not results["dependencies"]:
            print("\n📦 依赖安装:")
            print("   pip install telethon asyncio")
    
    print("="*60)
    
    return all_passed

def main():
    """主函数"""
    print("🔍 TG Realtime Forward 环境检查")
    print("="*60)
    
    success = generate_report()
    
    if not success:
        sys.exit(1)

if __name__ == "__main__":
    main()
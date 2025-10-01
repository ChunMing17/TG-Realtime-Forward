#!/usr/bin/env python3
"""
TG Realtime Forward 配置测试脚本
用于测试配置文件是否正确
"""

import sys
import os
import json

def test_config():
    """测试配置文件"""
    print("🧪 测试配置文件...")
    
    # 检查配置文件是否存在
    if not os.path.exists("config.py"):
        print("❌ 配置文件 config.py 不存在")
        print("💡 请复制 config_example.py 为 config.py 并进行配置")
        return False
    
    try:
        # 动态导入配置
        sys.path.insert(0, os.getcwd())
        import config
        
        print("✅ 配置文件加载成功")
        
        # 测试各个配置项
        test_results = {}
        
        # 测试账号配置
        print("\n📋 测试账号配置...")
        if hasattr(config, 'ACCOUNTS') and config.ACCOUNTS:
            print(f"   ✅ 找到 {len(config.ACCOUNTS)} 个账号配置")
            
            for i, account in enumerate(config.ACCOUNTS):
                if isinstance(account, dict):
                    required_keys = ['api_id', 'api_hash', 'session_name']
                    missing_keys = [key for key in required_keys if key not in account]
                    
                    if missing_keys:
                        print(f"   ❌ 账号 {i+1} 缺少配置: {missing_keys}")
                        test_results[f'account_{i+1}'] = False
                    else:
                        print(f"   ✅ 账号 {i+1}: {account['session_name']}")
                        test_results[f'account_{i+1}'] = True
                else:
                    print(f"   ❌ 账号 {i+1} 格式错误")
                    test_results[f'account_{i+1}'] = False
        else:
            print("   ❌ 未找到账号配置")
            test_results['accounts'] = False
        
        # 测试频道配置
        print("\n📺 测试频道配置...")
        if hasattr(config, 'PRESET_SOURCE_CHANNELS') and config.PRESET_SOURCE_CHANNELS:
            print(f"   ✅ 源频道: {len(config.PRESET_SOURCE_CHANNELS)} 个")
            for i, channel in enumerate(config.PRESET_SOURCE_CHANNELS):
                print(f"      {i+1}. {channel}")
            test_results['source_channels'] = True
        else:
            print("   ❌ 未配置源频道")
            test_results['source_channels'] = False
        
        if hasattr(config, 'PRESET_TARGET_CHANNEL') and config.PRESET_TARGET_CHANNEL:
            print(f"   ✅ 目标频道: {config.PRESET_TARGET_CHANNEL}")
            test_results['target_channel'] = True
        else:
            print("   ❌ 未配置目标频道")
            test_results['target_channel'] = False
        
        # 测试其他重要配置
        print("\n⚙️  测试其他配置...")
        important_configs = [
            ('ENABLE_REALTIME_FORWARD', '实时转发'),
            ('ENABLE_ACCOUNT_ROTATION', '账号轮换'),
            ('ENABLE_AD_FILTER', '广告过滤'),
            ('ENABLE_CONTENT_FILTER', '内容过滤'),
            ('ENABLE_CONTENT_DEDUPLICATION', '内容去重'),
        ]
        
        for config_name, description in important_configs:
            if hasattr(config, config_name):
                value = getattr(config, config_name)
                status = "启用" if value else "禁用"
                print(f"   {config_name} ({description}): {status}")
                test_results[config_name.lower()] = True
            else:
                print(f"   ❌ {config_name} 未找到")
                test_results[config_name.lower()] = False
        
        # 汇总结果
        print("\n📊 测试结果汇总:")
        print("-" * 40)
        
        all_passed = True
        for test, result in test_results.items():
            status = "✅ 通过" if result else "❌ 失败"
            print(f"   {test}: {status}")
            if not result:
                all_passed = False
        
        return all_passed
        
    except Exception as e:
        print(f"❌ 配置文件测试失败: {e}")
        return False

def test_dependencies():
    """测试依赖库"""
    print("\n📦 测试依赖库...")
    
    required_packages = [
        ('telethon', 'Telethon库'),
        ('asyncio', 'AsyncIO库'),
    ]
    
    all_good = True
    
    for package, description in required_packages:
        try:
            __import__(package)
            print(f"   ✅ {description}")
        except ImportError:
            print(f"   ❌ {description} - 未安装")
            all_good = False
    
    return all_good

def generate_test_report():
    """生成测试报告"""
    print("🧪 TG Realtime Forward 配置测试")
    print("="*50)
    
    config_ok = test_config()
    deps_ok = test_dependencies()
    
    print("\n" + "="*50)
    print("📋 测试报告")
    print("="*50)
    
    if config_ok and deps_ok:
        print("🎉 所有测试通过！")
        print("\n✅ 您的环境已准备就绪，可以运行程序了！")
        print("\n下一步:")
        print("   1. 运行 ./start_forward.sh (Linux/Mac)")
        print("   2. 或运行 start_forward.bat (Windows)")
        print("   3. 按照提示完成首次验证")
        return True
    else:
        print("⚠️  测试未完全通过")
        
        if not config_ok:
            print("\n🔧 配置问题:")
            print("   - 请检查 config.py 文件")
            print("   - 确保所有必要配置项都已填写")
            print("   - 参考 config_example.py 进行配置")
        
        if not deps_ok:
            print("\n📦 依赖问题:")
            print("   - 请安装缺失的依赖库")
            print("   - 运行: pip install telethon asyncio")
        
        return False

def main():
    """主函数"""
    success = generate_test_report()
    
    if not success:
        sys.exit(1)

if __name__ == "__main__":
    main()
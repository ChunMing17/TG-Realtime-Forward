#!/bin/bash

# TG Realtime Forward 启动脚本
# 用于Linux/Mac系统的便捷启动

echo "🚀 启动 TG Realtime Forward 服务..."
echo "======================================"

# 检查Python环境
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误: 未找到 Python3，请先安装 Python3"
    exit 1
fi

# 检查配置文件
if [ ! -f "config.py" ]; then
    echo "⚠️  未找到 config.py 配置文件"
    echo "📋 请复制 config_example.py 为 config.py 并进行配置"
    
    read -p "是否现在复制配置文件模板？(y/n): " choice
    if [ "$choice" = "y" ] || [ "$choice" = "Y" ]; then
        cp config_example.py config.py
        echo "✅ 配置文件模板已复制为 config.py"
        echo "📝 请编辑 config.py 文件配置您的账号和频道信息"
        echo "配置完成后重新运行此脚本"
        exit 0
    else
        echo "❌ 需要配置文件才能运行"
        exit 1
    fi
fi

# 检查依赖
echo "🔍 检查依赖..."
if ! python3 -c "import telethon" 2>/dev/null; then
    echo "⚠️  未找到 telethon 库，正在安装..."
    pip install telethon
fi

if ! python3 -c "import asyncio" 2>/dev/null; then
    echo "⚠️  未找到 asyncio 库，正在安装..."
    pip install asyncio
fi

echo "✅ 依赖检查完成"

# 启动模式选择
echo ""
echo "选择启动模式:"
echo "1. 前台运行 (推荐用于首次运行和调试)"
echo "2. 后台运行 (推荐用于长期运行)"
echo "3. 带日志重定向的后台运行"
echo ""

read -p "请选择 (1/2/3): " mode

case $mode in
    1)
        echo "🎯 前台运行模式"
        python3 TG_Realtime_Forward.py
        ;;
    2)
        echo "🌙 后台运行模式"
        nohup python3 TG_Realtime_Forward.py > /dev/null 2>&1 &
        echo "✅ 服务已在后台启动"
        echo "📄 日志文件: tg_realtime_forward.log"
        echo "🔍 查看日志: tail -f tg_realtime_forward.log"
        ;;
    3)
        echo "📝 带日志重定向的后台运行模式"
        log_file="forward_$(date +%Y%m%d_%H%M%S).log"
        nohup python3 TG_Realtime_Forward.py > "$log_file" 2>&1 &
        echo "✅ 服务已在后台启动"
        echo "📄 日志文件: $log_file"
        echo "🔍 查看日志: tail -f $log_file"
        ;;
    *)
        echo "❌ 无效选择，退出"
        exit 1
        ;;
esac

echo ""
echo "======================================"
echo "🎉 TG Realtime Forward 启动完成!"
echo ""
echo "📋 常用命令:"
echo "  查看运行状态: ps aux | grep TG_Realtime_Forward"
echo "  停止服务: pkill -f TG_Realtime_Forward"
echo "  查看日志: tail -f tg_realtime_forward.log"
echo "  查看统计: grep '转发成功' tg_realtime_forward.log | wc -l"
echo "======================================"
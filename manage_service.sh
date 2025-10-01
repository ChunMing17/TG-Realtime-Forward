#!/bin/bash

# TG Realtime Forward 管理服务脚本
# 用于管理服务的启动、停止、重启和监控

SCRIPT_NAME="TG_Realtime_Forward.py"
LOG_FILE="tg_realtime_forward.log"

# 显示使用帮助
show_help() {
    echo "TG Realtime Forward 管理服务脚本"
    echo "用法: $0 {start|stop|restart|status|logs|stats|help}"
    echo ""
    echo "命令说明:"
    echo "  start   - 启动服务"
    echo "  stop    - 停止服务"
    echo "  restart - 重启服务"
    echo "  status  - 查看服务状态"
    echo "  logs    - 查看实时日志"
    echo "  stats   - 查看转发统计"
    echo "  help    - 显示此帮助信息"
}

# 检查服务是否正在运行
is_running() {
    pgrep -f "$SCRIPT_NAME" > /dev/null
    return $?
}

# 启动服务
start_service() {
    if is_running; then
        echo "⚠️  服务已经在运行中"
        return 1
    fi
    
    echo "🚀 启动 TG Realtime Forward 服务..."
    
    if [ -f "start_forward.sh" ]; then
        ./start_forward.sh
    else
        echo "❌ 未找到启动脚本 start_forward.sh"
        return 1
    fi
}

# 停止服务
stop_service() {
    if ! is_running; then
        echo "⚠️  服务未在运行"
        return 1
    fi
    
    echo "🛑 停止服务..."
    pkill -f "$SCRIPT_NAME"
    
    # 等待服务完全停止
    for i in {1..10}; do
        if ! is_running; then
            echo "✅ 服务已停止"
            return 0
        fi
        echo -n "."
        sleep 1
    done
    
    echo ""
    echo "⚠️  服务停止超时，强制终止..."
    pkill -9 -f "$SCRIPT_NAME"
    echo "✅ 服务已强制停止"
}

# 重启服务
restart_service() {
    echo "🔄 重启服务..."
    stop_service
    sleep 2
    start_service
}

# 查看服务状态
show_status() {
    if is_running; then
        PID=$(pgrep -f "$SCRIPT_NAME")
        echo "✅ 服务正在运行 (PID: $PID)"
        
        # 显示进程信息
        ps aux | grep -E "$SCRIPT_NAME|python" | grep -v grep
        
        # 显示系统资源使用情况
        echo ""
        echo "系统资源使用情况:"
        top -p $PID -n 1 | tail -5
    else
        echo "❌ 服务未在运行"
    fi
}

# 查看实时日志
show_logs() {
    if [ -f "$LOG_FILE" ]; then
        echo "📄 查看实时日志 (按 Ctrl+C 退出):"
        tail -f "$LOG_FILE"
    else
        echo "⚠️  未找到日志文件: $LOG_FILE"
    fi
}

# 查看统计信息
show_stats() {
    if [ -f "$LOG_FILE" ]; then
        echo "📊 转发统计信息:"
        echo "=================="
        
        # 计算各种统计信息
        total_forwarded=$(grep -c "转发成功" "$LOG_FILE" 2>/dev/null || echo "0")
        total_errors=$(grep -c "ERROR" "$LOG_FILE" 2>/dev/null || echo "0")
        total_warnings=$(grep -c "WARNING" "$LOG_FILE" 2>/dev/null || echo "0")
        
        # 广告过滤统计
        ad_filtered=$(grep -c "过滤广告" "$LOG_FILE" 2>/dev/null || echo "0")
        content_filtered=$(grep -c "过滤无意义内容" "$LOG_FILE" 2>/dev/null || echo "0")
        duplicate_filtered=$(grep -c "跳过重复内容" "$LOG_FILE" 2>/dev/null || echo "0")
        
        # 账号轮换统计
        account_switches=$(grep -c "切换账号" "$LOG_FILE" 2>/dev/null || echo "0")
        
        # 重连统计
        reconnections=$(grep -c "重连" "$LOG_FILE" 2>/dev/null || echo "0")
        
        echo "📈 转发统计:"
        echo "  成功转发: $total_forwarded 条"
        echo "  广告过滤: $ad_filtered 条"
        echo "  内容过滤: $content_filtered 条"
        echo "  重复过滤: $duplicate_filtered 条"
        echo ""
        echo "🔧 运行统计:"
        echo "  账号切换: $account_switches 次"
        echo "  重连次数: $reconnections 次"
        echo "  错误次数: $total_errors 次"
        echo "  警告次数: $total_warnings 次"
        echo ""
        echo "📅 日志文件大小:"
        ls -lh "$LOG_FILE" | awk '{print $5}'
        
        # 显示最近的活动
        echo ""
        echo "🔥 最近5条转发记录:"
        grep "转发成功" "$LOG_FILE" | tail -5
        
    else
        echo "⚠️  未找到日志文件: $LOG_FILE"
    fi
}

# 主程序逻辑
case "$1" in
    start)
        start_service
        ;;
    stop)
        stop_service
        ;;
    restart)
        restart_service
        ;;
    status)
        show_status
        ;;
    logs)
        show_logs
        ;;
    stats)
        show_stats
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "❌ 未知命令: $1"
        echo ""
        show_help
        exit 1
        ;;
esac
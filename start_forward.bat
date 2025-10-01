@echo off
REM TG Realtime Forward 启动脚本 (Windows)
REM 用于Windows系统的便捷启动

echo 🚀 启动 TG Realtime Forward 服务...
echo ======================================

REM 检查Python环境
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo ❌ 错误: 未找到 Python，请先安装 Python
    exit /b 1
)

REM 检查配置文件
if not exist "config.py" (
    echo ⚠️  未找到 config.py 配置文件
    echo 📋 请复制 config_example.py 为 config.py 并进行配置
    
    set /p choice=是否现在复制配置文件模板？(y/n): 
    if /i "%choice%"=="y" (
        copy config_example.py config.py
        echo ✅ 配置文件模板已复制为 config.py
        echo 📝 请编辑 config.py 文件配置您的账号和频道信息
        echo 配置完成后重新运行此脚本
        exit /b 0
    ) else (
        echo ❌ 需要配置文件才能运行
        exit /b 1
    )
)

REM 检查依赖
echo 🔍 检查依赖...
python -c "import telethon" 2>nul
if %errorlevel% neq 0 (
    echo ⚠️  未找到 telethon 库，正在安装...
    pip install telethon
)

python -c "import asyncio" 2>nul
if %errorlevel% neq 0 (
    echo ⚠️  未找到 asyncio 库，正在安装...
    pip install asyncio
)

echo ✅ 依赖检查完成

REM 启动模式选择
echo.
echo 选择启动模式:
echo 1. 前台运行 (推荐用于首次运行和调试)
echo 2. 后台运行 (推荐用于长期运行)
echo.

set /p mode=请选择 (1/2): 

if "%mode%"=="1" (
    echo 🎯 前台运行模式
    python TG_Realtime_Forward.py
) else if "%mode%"=="2" (
    echo 🌙 后台运行模式
    set log_file=forward_%date:~-4,4%%date:~-10,2%%date:~-7,2%_%time:~0,2%%time:~3,2%%time:~6,2%.log
    set log_file=%log_file: =0%
    start /min cmd /c "python TG_Realtime_Forward.py > %log_file% 2>&1"
    echo ✅ 服务已在后台启动
    echo 📄 日志文件: %log_file%
    echo 🔍 查看日志: type %log_file%
) else (
    echo ❌ 无效选择，退出
    exit /b 1
)

echo.
echo ======================================
echo 🎉 TG Realtime Forward 启动完成!
echo.
echo 📋 常用命令:
echo   查看运行状态: tasklist ^| findstr python
echo   停止服务: taskkill /f /im python.exe
echo   查看日志: type tg_realtime_forward.log
echo   查看统计: find /c "转发成功" tg_realtime_forward.log
echo ======================================

pause
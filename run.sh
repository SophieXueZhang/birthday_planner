#!/bin/bash
# 生日派对计划工具启动脚本

echo "检查Python版本..."
python3 --version

echo ""
echo "检查依赖..."
if ! python3 -c "import rich" 2>/dev/null; then
    echo "正在安装依赖..."
    pip install -r requirements.txt
fi

echo ""
echo "启动生日派对计划工具..."
cd src && python3 main.py

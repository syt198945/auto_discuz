#!/bin/bash

echo "========================================"
echo "ZelosTech 论坛自动化工具"
echo "========================================"
echo

echo "正在检查 Python 环境..."
python3 --version
if [ $? -ne 0 ]; then
    echo "错误: 未找到 Python，请先安装 Python 3.7+"
    exit 1
fi

echo
echo "正在安装依赖包..."
pip3 install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "错误: 依赖包安装失败"
    exit 1
fi

echo
echo "依赖包安装完成！"
echo
echo "正在启动论坛自动化工具..."
python3 run_local.py


#!/bin/bash

# 从 .env 加载虚拟环境配置
while IFS='=' read -r key value; do
    if [ "$key" = "CONDA_ENV_NAME" ]; then
        CONDA_ENV_NAME="$value"
    elif [ "$key" = "CONDA_ENV_PATH" ]; then
        CONDA_ENV_PATH="$value"
    fi
done < .env

# 激活conda环境（Ubuntu中conda激活路径与Windows不同）
source "$CONDA_ENV_PATH/bin/activate" "$CONDA_ENV_PATH"
conda activate "$CONDA_ENV_NAME"

echo "已激活环境：$CONDA_ENV_NAME"

# 运行uvicorn服务（参数与原命令一致）
uvicorn main:app --reload --host 0.0.0.0 --port 8000
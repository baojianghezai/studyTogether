#!/bin/bash
export PYTHONPATH=/root/studyTogether:$PYTHONPATH
# 激活conda环境（Ubuntu中conda激活路径与Windows不同）
source "/opt/miniconda3/bin/activate" "studyTogether"

echo "已激活环境：$CONDA_ENV_NAME"

# 运行uvicorn服务（参数与原命令一致）
uvicorn main:app --host 0.0.0.0 --port 8000
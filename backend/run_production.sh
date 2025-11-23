#!/bin/bash

# Backend 서버 실행 스크립트 (프로덕션)
# 항상 실행되도록 설정

cd "$(dirname "$0")"
export PYTHONPATH="${PYTHONPATH}:$(pwd)/.."

# 가상환경 활성화
if [ -d "../venv" ]; then
    source ../venv/bin/activate
elif [ -d "venv" ]; then
    source venv/bin/activate
fi

# 프로덕션 모드로 실행 (reload 없음)
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4


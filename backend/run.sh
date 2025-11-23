#!/bin/bash

# Backend 서버 실행 스크립트
# 개발 환경용

cd "$(dirname "$0")"
export PYTHONPATH="${PYTHONPATH}:$(pwd)/.."

# 가상환경 활성화 (있는 경우)
if [ -d "../venv" ]; then
    source ../venv/bin/activate
elif [ -d "venv" ]; then
    source venv/bin/activate
fi

# 서버 실행
uvicorn main:app --host 0.0.0.0 --port 8000 --reload


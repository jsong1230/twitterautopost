#!/bin/bash

# 맥에서 백엔드 서버 실행 스크립트

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

# 가상환경 활성화
source venv/bin/activate

# Python 경로 설정 (프로젝트 루트를 경로에 추가)
export PYTHONPATH="${PYTHONPATH}:${SCRIPT_DIR}"

# Backend 디렉토리로 이동
cd backend

# 서버 실행
echo "🚀 Backend 서버 시작 중..."
echo "📍 서버 주소: http://localhost:8000"
echo "📚 API 문서: http://localhost:8000/docs"
echo "💚 Health check: http://localhost:8000/health"
echo ""
echo "서버를 중지하려면 Ctrl+C를 누르세요."
echo ""

uvicorn main:app --host 0.0.0.0 --port 8000 --reload


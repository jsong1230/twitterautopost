#!/usr/bin/env python3
"""
Backend 서버 실행 스크립트 (Python)
개발 및 프로덕션 환경 모두 지원
"""

import sys
import os
import uvicorn

# 프로젝트 루트를 Python 경로에 추가
backend_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(backend_dir)
sys.path.insert(0, project_root)

if __name__ == "__main__":
    # 환경 변수로 모드 설정 (기본값: 개발 모드)
    is_production = os.getenv("PRODUCTION", "false").lower() == "true"
    port = int(os.getenv("PORT", "8000"))
    host = os.getenv("HOST", "0.0.0.0")
    
    if is_production:
        # 프로덕션: 여러 워커 사용, reload 없음
        uvicorn.run(
            "main:app",
            host=host,
            port=port,
            workers=4,
            log_level="info"
        )
    else:
        # 개발: 단일 워커, reload 활성화
        uvicorn.run(
            "main:app",
            host=host,
            port=port,
            reload=True,
            log_level="debug"
        )


# 빠른 시작 가이드 (맥)

## 🚀 서버 실행 방법

### 방법 1: 실행 스크립트 사용 (권장)

```bash
# 프로젝트 루트에서
./run_backend.sh
```

### 방법 2: 직접 실행

```bash
# 가상환경 활성화
source venv/bin/activate

# Backend 디렉토리로 이동
cd backend

# Python 경로 설정
export PYTHONPATH="${PYTHONPATH}:$(cd .. && pwd)"

# 서버 실행
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### 방법 3: Python 스크립트 사용

```bash
source venv/bin/activate
cd backend
python start_server.py
```

## ✅ 서버 확인

서버가 실행되면 다음 주소에서 확인할 수 있습니다:

- **서버**: http://localhost:8000
- **API 문서**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## 🔧 문제 해결

### 포트가 이미 사용 중인 경우

```bash
# 포트 8000을 사용하는 프로세스 확인
lsof -i :8000

# 프로세스 종료
kill -9 <PID>
```

### 가상환경이 활성화되지 않는 경우

```bash
# 가상환경 재생성
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 모듈을 찾을 수 없는 경우

```bash
# Python 경로 확인
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

## 📝 참고사항

- 서버는 **24시간 실행**되어야 스케줄러가 작동합니다
- 개발 중에는 `--reload` 옵션으로 자동 재시작됩니다
- 프로덕션에서는 `run_production.sh`를 사용하거나 systemd/supervisor를 사용하세요


# 시작하기 가이드

프로젝트를 시작하기 위해 필요한 모든 정보를 정리했습니다.

## 🔑 필수 환경 변수

프로젝트 루트에 `.env` 파일을 생성하고 다음 변수들을 설정하세요:

```env
# OpenAI API (선택사항 - 더미 데이터로도 테스트 가능)
OPENAI_API_KEY=your_openai_api_key_here

# Claude API (선택사항 - 더미 데이터로도 테스트 가능)
CLAUDE_API_KEY=your_claude_api_key_here

# Twitter API Bearer Token (선택사항 - 더미 데이터로도 테스트 가능)
TWITTER_BEARER_TOKEN=your_twitter_bearer_token_here

# 데이터베이스 (기본값 사용 가능)
DATABASE_URL=sqlite:///./twitter_insights.db

# 서버 설정 (기본값 사용 가능)
BACKEND_PORT=8000
BACKEND_HOST=0.0.0.0

# 스케줄러 설정 (기본값 사용 가능)
ENABLE_SCHEDULER=true
SCHEDULER_HOURS=9,15,21
```

**중요**: API 키가 없어도 더미 데이터로 개발 및 테스트가 가능합니다!

## 🚀 서버 실행 방법

### 맥에서 실행

```bash
# 방법 1: 실행 스크립트 사용 (가장 간단)
./run_backend.sh

# 방법 2: 직접 실행
source venv/bin/activate
cd backend
export PYTHONPATH="${PYTHONPATH}:$(cd .. && pwd)"
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### 서버 확인

서버가 실행되면 다음 주소에서 확인할 수 있습니다:

- **서버**: http://localhost:8000
- **API 문서 (Swagger)**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## 📡 주요 API 엔드포인트

### 키워드 관리

```bash
# 키워드 목록 조회
GET /api/keywords/

# 키워드 추가
POST /api/keywords/
Body: { "keyword": "AI" }

# 키워드 삭제
DELETE /api/keywords/{keyword_id}

# 키워드 활성/비활성 토글
PATCH /api/keywords/{keyword_id}/toggle
```

### 인사이트 생성 및 조회

```bash
# 인사이트 목록 조회
GET /api/insights/

# 특정 키워드에 대한 인사이트 생성 (수동)
POST /api/insights/generate/{keyword_id}

# 특정 인사이트 조회
GET /api/insights/{insight_id}
```

### 포스트 조회

```bash
# 포스트 목록 조회
GET /api/posts/

# 특정 인사이트의 포스트 조회
GET /api/posts/?insight_id={insight_id}
```

## 🗄️ 데이터베이스

- **위치**: `backend/twitter_insights.db`
- **타입**: SQLite
- **자동 생성**: 서버 시작 시 자동으로 생성됩니다

### 주요 테이블

1. **keywords**: 등록된 키워드
   - `id`, `keyword`, `is_active`, `created_at`, `updated_at`

2. **insights**: 생성된 인사이트
   - `id`, `keyword_id`, `keyword`, `summary_kr`, `summary_en`, `tweets_analyzed`, `created_at`

3. **posts**: 생성된 포스트 (트윗/인스타그램)
   - `id`, `insight_id`, `post_type`, `content`, `hashtags`, `created_at`

## ⏰ 스케줄러 설정

### 기본 동작

- **실행 시간**: 매일 9시, 15시, 21시
- **대상**: 활성화된 모든 키워드 (`is_active=true`)
- **동작**: 각 키워드에 대해 트윗 수집 → AI 분석 → 인사이트 생성 → 포스트 생성

### 스케줄러 비활성화

`.env` 파일에서:
```env
ENABLE_SCHEDULER=false
```

### 실행 시간 변경

`.env` 파일에서:
```env
# 매 6시간마다 실행
SCHEDULER_HOURS=0,6,12,18

# 매일 오전 9시에만 실행
SCHEDULER_HOURS=9
```

## 📝 사용 흐름

### 1. 키워드 등록

```bash
curl -X POST "http://localhost:8000/api/keywords/" \
  -H "Content-Type: application/json" \
  -d '{"keyword": "AI"}'
```

### 2. 인사이트 생성 (수동)

```bash
curl -X POST "http://localhost:8000/api/insights/generate/1"
```

### 3. 인사이트 조회

```bash
curl "http://localhost:8000/api/insights/"
```

### 4. 생성된 포스트 확인

```bash
curl "http://localhost:8000/api/posts/?insight_id=1"
```

## 🔧 개발 팁

### API 테스트

1. 브라우저에서 http://localhost:8000/docs 접속
2. Swagger UI에서 모든 API를 테스트할 수 있습니다
3. "Try it out" 버튼을 클릭하여 직접 테스트

### 로그 확인

서버 실행 시 콘솔에 로그가 출력됩니다:
- 스케줄러 시작/종료
- 인사이트 생성 진행 상황
- 에러 메시지

### 더미 데이터

API 키가 없어도:
- Twitter 서비스는 더미 트윗 데이터를 반환합니다
- AI 서비스는 더미 인사이트를 생성합니다
- 전체 흐름을 테스트할 수 있습니다

## 📂 주요 파일 위치

- **백엔드 진입점**: `backend/main.py`
- **설정 파일**: `backend/config.py`
- **데이터베이스**: `backend/database.py`
- **API 라우터**: `backend/routers/`
- **비즈니스 로직**: `backend/services/`
- **데이터 모델**: `backend/models/`

## 🐛 문제 해결

### 포트가 이미 사용 중

```bash
# 포트 사용 확인
lsof -i :8000

# 프로세스 종료
kill -9 <PID>
```

### 모듈을 찾을 수 없음

```bash
# Python 경로 확인
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

### 데이터베이스 오류

```bash
# 데이터베이스 파일 삭제 후 재시작 (주의: 모든 데이터 삭제됨)
rm backend/twitter_insights.db
# 서버 재시작 시 자동으로 재생성됨
```

## 📚 추가 문서

- **DEVELOPMENT.md**: 상세한 개발 가이드
- **RULES.md**: 개발 규칙 및 컨벤션
- **TODO.md**: 할 일 목록 및 진행 중인 작업
- **HISTORY.md**: 프로젝트 히스토리 및 완료된 작업
- **PRODUCTION.md**: 프로덕션 배포 가이드
- **QUICKSTART.md**: 빠른 시작 가이드

## 🎯 다음 단계

1. ✅ 서버 실행 확인
2. ⏭️ API 문서에서 엔드포인트 테스트
3. ⏭️ 키워드 추가 및 인사이트 생성 테스트
4. ⏭️ Frontend 개발 시작 (필요시)


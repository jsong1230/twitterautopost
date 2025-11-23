# Twitter/Instagram AI 기반 인사이트 & 포스트 생성기

Twitter(X)와 Instagram용 AI 기반 인사이트 및 포스트 자동 생성 웹 서비스입니다.

## 📋 목차

- [기능](#-기능)
- [기술 스택](#-기술-스택)
- [빠른 시작](#-빠른-시작)
- [프로젝트 구조](#-프로젝트-구조)
- [개발 가이드](#-개발-가이드)
- [배포](#-배포)
- [문서](#-문서)

## ✨ 기능

- 키워드 기반 트윗 수집 및 분석
- AI 기반 트렌드 요약 (한글/영어)
- 트윗 초안 자동 생성 (3-5개)
- 인스타그램 캡션 + 해시태그 자동 생성
- 웹 UI를 통한 키워드 관리 및 결과 조회
- **주기적 자동 인사이트 생성** (매일 9시, 15시, 21시)

## 🛠 기술 스택

- **Backend**: Python 3.9+ + FastAPI
- **Frontend**: Next.js 14+ (TypeScript, App Router)
- **Database**: SQLite (SQLAlchemy)
- **AI**: OpenAI API, Claude API
- **스케줄러**: APScheduler

## 🚀 빠른 시작

### 필수 요구사항

- Python 3.9 이상
- Node.js 18 이상
- npm 또는 yarn

### 설치 및 실행

### 1. 저장소 클론

```bash
git clone <repository-url>
cd twitterautopost
```

### 2. Backend 설정

```bash
# Python 가상환경 생성
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 의존성 설치
pip install -r requirements.txt
```

### 3. Frontend 설정

```bash
cd frontend
npm install
cd ..
```

### 4. 환경 변수 설정

```bash
# .env 파일 생성
cp .env.example .env

# .env 파일 편집하여 API 키 입력
# OPENAI_API_KEY=your_key_here
# CLAUDE_API_KEY=your_key_here
# TWITTER_BEARER_TOKEN=your_token_here
```

**참고**: API 키가 없어도 더미 데이터로 개발 및 테스트가 가능합니다.

### 실행

**Backend (개발 모드):**
```bash
cd backend
./run.sh
# 또는
python start_server.py
# 또는 직접
uvicorn main:app --reload --port 8000
```

서버는 `http://localhost:8000`에서 실행됩니다.
API 문서는 `http://localhost:8000/docs`에서 확인할 수 있습니다.

**Backend (프로덕션 모드 - 항상 켜져있게):**
```bash
cd backend
./run_production.sh
# 또는
PRODUCTION=true python start_server.py
```

프로덕션 환경에서는 systemd, supervisor, PM2 등을 사용하여 항상 실행되도록 설정하세요.
자세한 내용은 `infra/README.md`를 참고하세요.

**Frontend:**
```bash
cd frontend
npm run dev
```

### 5. 서버 실행

**Backend (터미널 1):**
```bash
cd backend
./run.sh
# 또는
python start_server.py
# 또는 직접
uvicorn main:app --reload --port 8000
```

서버는 `http://localhost:8000`에서 실행됩니다.
- API 문서: `http://localhost:8000/docs`
- Health check: `http://localhost:8000/health`

**Frontend (터미널 2):**
```bash
cd frontend
npm run dev
```

프론트엔드는 `http://localhost:3000`에서 실행됩니다.

## 📁 프로젝트 구조

```
twitterautopost/
├── backend/                    # FastAPI 백엔드 서버
│   ├── main.py                # FastAPI 앱 진입점
│   ├── config.py              # 설정 관리
│   ├── database.py            # DB 연결 및 세션 관리
│   ├── start_server.py        # 서버 실행 스크립트
│   ├── run.sh                 # 개발용 실행 스크립트
│   ├── run_production.sh      # 프로덕션용 실행 스크립트
│   ├── models/                # SQLAlchemy 모델
│   │   ├── keyword.py         # 키워드 모델
│   │   ├── insight.py         # 인사이트 모델
│   │   └── post.py            # 포스트 모델
│   ├── routers/               # API 라우터
│   │   ├── keywords.py        # 키워드 CRUD API
│   │   ├── insights.py        # 인사이트 생성/조회 API
│   │   └── posts.py           # 포스트 조회 API
│   └── services/              # 비즈니스 로직
│       ├── ai_service.py       # OpenAI/Claude API 연동
│       ├── twitter_service.py # Twitter API 연동
│       └── scheduler_service.py # 주기적 작업 스케줄러
├── frontend/                  # Next.js 프론트엔드
│   ├── app/                   # App Router 페이지
│   ├── components/            # React 컴포넌트
│   └── lib/                   # 유틸리티 함수
├── infra/                     # 배포 설정
│   ├── systemd/               # systemd 서비스 파일
│   ├── supervisor/            # supervisor 설정
│   └── README.md              # 배포 가이드
├── requirements.txt           # Python 의존성
├── .env.example               # 환경 변수 예시
├── README.md                  # 이 파일
├── DEVELOPMENT.md             # 개발 가이드
├── RULES.md                   # 개발 규칙
├── TODO.md                    # 할 일 목록
└── HISTORY.md                  # 프로젝트 히스토리
```

## 📚 문서

- **[DEVELOPMENT.md](./DEVELOPMENT.md)**: 상세한 개발 가이드
- **[RULES.md](./RULES.md)**: 개발 규칙 및 컨벤션
- **[TODO.md](./TODO.md)**: 할 일 목록 및 진행 중인 작업
- **[HISTORY.md](./HISTORY.md)**: 프로젝트 히스토리 및 완료된 작업
- **[GETTING_STARTED.md](./GETTING_STARTED.md)**: 시작하기 가이드
- **[QUICKSTART.md](./QUICKSTART.md)**: 빠른 시작 가이드
- **[PRODUCTION.md](./PRODUCTION.md)**: 프로덕션 배포 가이드
- **[infra/README.md](./infra/README.md)**: 배포 설정 가이드

## 🔄 서버 실행 모드

### 개발 모드
- 자동 재시작 (코드 변경 시)
- 디버그 로깅
- 단일 워커
- 스케줄러 자동 시작

### 프로덕션 모드 (24시간 실행)
- **항상 켜져있는 서버 필요** ⚠️
- 여러 워커 사용 (성능 향상)
- 자동 재시작 없음
- systemd/supervisor/PM2로 관리
- 스케줄러가 매일 지정된 시간에 자동 실행

**중요**: 이 서비스는 24시간 실행되어야 합니다. 스케줄러가 주기적으로 인사이트를 생성합니다.

자세한 배포 방법은 다음 문서를 참고하세요:
- **[PRODUCTION.md](./PRODUCTION.md)**: 상세한 프로덕션 배포 가이드
- **[infra/README.md](./infra/README.md)**: 배포 설정 파일 설명

## 🎯 주요 기능 설명

### 키워드 관리
- 키워드 추가/삭제/조회
- 키워드 활성/비활성 토글
- 활성화된 키워드에 대해 자동으로 인사이트 생성

### 자동 인사이트 생성
- **스케줄러**: 매일 9시, 15시, 21시에 실행
- 활성화된 모든 키워드에 대해 트윗 수집 및 분석
- AI를 통한 트렌드 요약 생성
- 트윗 초안 및 인스타그램 포스트 자동 생성

### 수동 인사이트 생성
- API를 통해 특정 키워드에 대해 즉시 인사이트 생성 가능
- `/api/insights/generate/{keyword_id}` 엔드포인트 사용

## 🔧 개발 시작하기

다른 머신이나 IDE에서 개발을 시작하려면:

1. **GETTING_STARTED.md** 또는 **QUICKSTART.md**를 먼저 읽어보세요
2. **DEVELOPMENT.md**에서 상세한 개발 가이드를 확인하세요
3. **RULES.md**에서 개발 규칙을 확인하세요
4. **TODO.md**에서 현재 할 일을 확인하세요
5. **HISTORY.md**에서 완료된 작업을 확인하세요

## 📞 문의

프로젝트 관련 문의사항이 있으면 이슈를 생성하거나 팀에 문의하세요.


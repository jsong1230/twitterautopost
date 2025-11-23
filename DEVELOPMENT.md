# 개발 가이드

이 문서는 프로젝트 개발을 시작하기 위한 상세한 가이드입니다.

## 🚀 빠른 시작

### 1. 저장소 클론 및 환경 설정

```bash
# 저장소 클론
git clone <repository-url>
cd twitterautopost

# Python 가상환경 생성 및 활성화
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Python 의존성 설치
pip install -r requirements.txt

# Node.js 의존성 설치
cd frontend
npm install
cd ..
```

### 2. 환경 변수 설정

```bash
# .env 파일 생성
cp .env.example .env

# .env 파일 편집하여 API 키 입력
# OPENAI_API_KEY=your_key_here
# CLAUDE_API_KEY=your_key_here
# TWITTER_BEARER_TOKEN=your_token_here
```

**참고**: API 키가 없어도 더미 데이터로 개발 및 테스트가 가능합니다.

### 3. 데이터베이스 초기화

데이터베이스는 서버 시작 시 자동으로 초기화됩니다. 별도 작업이 필요 없습니다.

### 4. 서버 실행

**Backend (터미널 1):**
```bash
cd backend
./run.sh
# 또는
python start_server.py
```

서버는 `http://localhost:8000`에서 실행됩니다.
API 문서: `http://localhost:8000/docs`

**Frontend (터미널 2):**
```bash
cd frontend
npm run dev
```

프론트엔드는 `http://localhost:3000`에서 실행됩니다.

## 📁 프로젝트 구조

```
twitterautopost/
├── backend/                    # FastAPI 백엔드
│   ├── main.py                # FastAPI 앱 진입점
│   ├── config.py              # 설정 관리 (환경 변수)
│   ├── database.py            # DB 연결 및 세션
│   ├── start_server.py        # 서버 실행 스크립트
│   ├── run.sh                 # 개발용 실행 스크립트
│   ├── run_production.sh      # 프로덕션용 실행 스크립트
│   ├── models/                # SQLAlchemy 모델
│   │   ├── __init__.py
│   │   ├── keyword.py         # 키워드 모델
│   │   ├── insight.py         # 인사이트 모델
│   │   └── post.py            # 포스트 모델
│   ├── routers/               # API 라우터
│   │   ├── __init__.py
│   │   ├── keywords.py        # 키워드 CRUD API
│   │   ├── insights.py        # 인사이트 생성/조회 API
│   │   └── posts.py           # 포스트 조회 API
│   └── services/              # 비즈니스 로직
│       ├── __init__.py
│       ├── ai_service.py      # AI API 연동 (OpenAI/Claude)
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
├── .gitignore                 # Git 무시 파일
├── README.md                  # 프로젝트 개요
├── DEVELOPMENT.md             # 이 문서
├── RULES.md                   # 개발 규칙
├── TODO.md                    # 할 일 목록
└── HISTORY.md                  # 프로젝트 히스토리
```

## 🔧 개발 환경 설정

### Python 환경

- **Python 버전**: 3.9 이상 권장
- **패키지 관리**: pip + requirements.txt
- **가상환경**: venv 사용 권장

### Node.js 환경

- **Node.js 버전**: 18 이상 권장
- **패키지 관리**: npm
- **프레임워크**: Next.js 14+ (App Router)

### IDE 설정

#### VS Code 권장 확장 프로그램
- Python
- Pylance
- ESLint
- Prettier
- Tailwind CSS IntelliSense

#### VS Code 설정 (`.vscode/settings.json`)
```json
{
  "python.defaultInterpreterPath": "${workspaceFolder}/venv/bin/python",
  "python.linting.enabled": true,
  "python.formatting.provider": "black",
  "[python]": {
    "editor.defaultFormatter": "ms-python.black-formatter"
  },
  "[typescript]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  }
}
```

## 🧪 테스트

### Backend 테스트

```bash
cd backend
pytest  # (향후 구현 예정)
```

### Frontend 테스트

```bash
cd frontend
npm test  # (향후 구현 예정)
```

## 📝 코드 스타일

### Python
- **포맷터**: Black (권장)
- **린터**: flake8 또는 pylint
- **타입 힌팅**: 가능한 모든 곳에 사용

### TypeScript/JavaScript
- **포맷터**: Prettier
- **린터**: ESLint
- **타입**: TypeScript strict mode

## 🔄 Git 워크플로우

### 브랜치 전략
- `main`: 프로덕션 배포용
- `develop`: 개발 통합 브랜치
- `feature/*`: 기능 개발 브랜치
- `fix/*`: 버그 수정 브랜치

### 커밋 메시지 규칙
```
<type>: <subject>

<body>

<footer>
```

**Type**: feat, fix, docs, style, refactor, test, chore

**예시**:
```
feat: 키워드 CRUD API 구현

- 키워드 추가/삭제/조회 기능 구현
- 중복 키워드 검증 추가
```

## 🐛 디버깅

### Backend 디버깅
- 로그는 `logging` 모듈 사용
- 개발 모드에서는 `--reload` 옵션으로 자동 재시작
- FastAPI 자동 생성 API 문서 활용 (`/docs`)

### Frontend 디버깅
- React DevTools 사용
- Next.js 개발 모드에서 핫 리로드
- 브라우저 개발자 도구 활용

## 📦 배포

자세한 배포 가이드는 `infra/README.md`를 참고하세요.

### 프로덕션 체크리스트
- [ ] 환경 변수 설정 확인
- [ ] 데이터베이스 백업
- [ ] API 키 검증
- [ ] 로깅 설정 확인
- [ ] 모니터링 설정
- [ ] 스케줄러 동작 확인

## 🔗 유용한 링크

- [FastAPI 문서](https://fastapi.tiangolo.com/)
- [Next.js 문서](https://nextjs.org/docs)
- [SQLAlchemy 문서](https://docs.sqlalchemy.org/)
- [OpenAI API 문서](https://platform.openai.com/docs)
- [Anthropic Claude API 문서](https://docs.anthropic.com/)

## ❓ 문제 해결

### 일반적인 문제

**Q: Backend 서버가 시작되지 않아요**
- Python 가상환경이 활성화되어 있는지 확인
- `requirements.txt`의 모든 패키지가 설치되었는지 확인
- 포트 8000이 이미 사용 중인지 확인

**Q: Frontend에서 API 호출이 실패해요**
- Backend 서버가 실행 중인지 확인
- CORS 설정 확인
- API 엔드포인트 URL 확인

**Q: 데이터베이스 오류가 발생해요**
- 데이터베이스 파일 권한 확인
- SQLite 버전 확인
- 데이터베이스 파일이 손상되지 않았는지 확인

## 📞 문의

프로젝트 관련 문의사항이 있으면 이슈를 생성하거나 팀에 문의하세요.


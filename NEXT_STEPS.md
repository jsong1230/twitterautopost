# 다음 단계 가이드

현재 프로젝트 상태와 다음에 해야 할 작업을 정리했습니다.

## 📊 현재 상태

### ✅ 완료된 작업
- Backend API 완전 구현 (FastAPI)
- AI 서비스 실제 연동 (OpenAI, Claude)
- 데이터베이스 모델 및 스키마
- 스케줄러 구현
- API 문서 및 테스트 가능

### 🚧 다음 단계: Frontend 구현

Frontend가 아직 구현되지 않았습니다. 다음 순서로 진행하세요.

## 🎯 우선순위별 작업

### 1단계: Frontend 기본 설정 (필수)

#### 1.1 API 클라이언트 설정
```bash
cd frontend
npm install axios  # 또는 fetch 사용
```

**작업 내용:**
- [ ] API 클라이언트 유틸리티 생성 (`lib/api.ts`)
- [ ] 환경 변수 설정 (API 베이스 URL)
- [ ] 에러 핸들링 유틸리티

**파일 위치:**
- `frontend/lib/api.ts` - API 클라이언트
- `frontend/lib/types.ts` - TypeScript 타입 정의

#### 1.2 공통 컴포넌트 생성
- [ ] Button 컴포넌트
- [ ] Input 컴포넌트
- [ ] Card 컴포넌트
- [ ] Loading 컴포넌트
- [ ] CopyButton 컴포넌트

**파일 위치:**
- `frontend/components/ui/`

### 2단계: 키워드 관리 페이지 (핵심 기능)

#### 2.1 키워드 목록 페이지 (`/keywords`)
- [ ] 키워드 목록 표시
- [ ] 키워드 추가 폼
- [ ] 키워드 삭제 기능
- [ ] 키워드 활성/비활성 토글
- [ ] 실시간 업데이트

**API 엔드포인트:**
- `GET /api/keywords/` - 목록 조회
- `POST /api/keywords/` - 키워드 추가
- `DELETE /api/keywords/{id}` - 키워드 삭제
- `PATCH /api/keywords/{id}/toggle` - 활성/비활성 토글

**파일 위치:**
- `frontend/app/keywords/page.tsx`
- `frontend/components/keywords/KeywordList.tsx`
- `frontend/components/keywords/KeywordForm.tsx`

### 3단계: 대시보드 페이지 (핵심 기능)

#### 3.1 대시보드 메인 페이지 (`/dashboard`)
- [ ] 오늘 생성된 인사이트 목록
- [ ] 생성된 포스트 목록 (트윗/인스타그램)
- [ ] Copy 버튼 기능
- [ ] 필터링 (날짜, 키워드별)
- [ ] 인사이트 생성 버튼 (수동)

**API 엔드포인트:**
- `GET /api/insights/` - 인사이트 목록
- `GET /api/posts/` - 포스트 목록
- `POST /api/insights/generate/{keyword_id}` - 인사이트 생성

**파일 위치:**
- `frontend/app/dashboard/page.tsx`
- `frontend/components/dashboard/InsightList.tsx`
- `frontend/components/dashboard/PostList.tsx`
- `frontend/components/dashboard/CopyButton.tsx`

### 4단계: 레이아웃 및 네비게이션

#### 4.1 메인 레이아웃
- [ ] 네비게이션 바
- [ ] 사이드바 (선택사항)
- [ ] 푸터
- [ ] 반응형 디자인

**파일 위치:**
- `frontend/components/layout/Navbar.tsx`
- `frontend/components/layout/Sidebar.tsx`
- `frontend/app/layout.tsx` 수정

#### 4.2 홈 페이지
- [ ] 프로젝트 소개
- [ ] 빠른 링크
- [ ] 통계 요약 (선택사항)

**파일 위치:**
- `frontend/app/page.tsx`

## 📝 구현 순서 추천

### 빠른 MVP 완성 (1-2일)
1. ✅ API 클라이언트 설정
2. ✅ 키워드 관리 페이지
3. ✅ 대시보드 기본 페이지
4. ✅ Copy 버튼 기능

### 완성도 높이기 (3-5일)
5. ✅ 레이아웃 및 네비게이션
6. ✅ 에러 핸들링 및 로딩 상태
7. ✅ 반응형 디자인
8. ✅ UI/UX 개선

## 🛠 기술 스택 (Frontend)

- **Framework**: Next.js 16 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS (이미 설정됨)
- **HTTP Client**: axios 또는 fetch
- **State Management**: React Hooks (useState, useEffect)

## 📋 체크리스트

### 필수 기능
- [ ] 키워드 CRUD
- [ ] 인사이트 조회
- [ ] 포스트 조회
- [ ] Copy 버튼

### 선택 기능
- [ ] 인사이트 상세 보기
- [ ] 포스트 상세 보기
- [ ] 필터링 및 검색
- [ ] 정렬 기능
- [ ] 페이지네이션

## 🚀 시작하기

1. **API 클라이언트부터 시작**
   ```bash
   cd frontend
   npm install axios
   ```

2. **타입 정의 생성**
   - Backend API 응답 타입 정의
   - `frontend/lib/types.ts` 생성

3. **첫 번째 페이지 구현**
   - 키워드 관리 페이지부터 시작 권장
   - 가장 간단하고 핵심 기능

## 💡 팁

- Backend API 문서 활용: http://localhost:8000/docs
- 컴포넌트는 작게 나누어 재사용 가능하게
- TypeScript 타입을 먼저 정의하면 개발이 수월함
- Tailwind CSS로 빠르게 스타일링

## 📚 참고 문서

- [Next.js 공식 문서](https://nextjs.org/docs)
- [Tailwind CSS 문서](https://tailwindcss.com/docs)
- [TypeScript 핸드북](https://www.typescriptlang.org/docs/)


# 개발 규칙 및 컨벤션

이 문서는 프로젝트 개발 시 따라야 할 규칙과 컨벤션을 정의합니다.

## 📋 일반 규칙

### 1. 코드 리뷰
- 모든 코드는 리뷰를 거쳐야 합니다.
- 최소 1명 이상의 승인이 필요합니다.

### 2. 테스트
- 새로운 기능은 테스트를 포함해야 합니다.
- 기존 기능 수정 시 관련 테스트도 업데이트해야 합니다.

### 3. 문서화
- 새로운 API 엔드포인트는 문서화해야 합니다.
- 복잡한 로직은 주석으로 설명해야 합니다.
- README와 관련 문서를 업데이트해야 합니다.

## 🐍 Python (Backend) 규칙

### 코드 스타일
- **PEP 8** 스타일 가이드 준수
- **Black** 포맷터 사용 (라인 길이 100자)
- **타입 힌팅** 필수 사용

### 네이밍 컨벤션
- **함수/변수**: `snake_case`
- **클래스**: `PascalCase`
- **상수**: `UPPER_SNAKE_CASE`
- **프라이빗**: `_leading_underscore`

### 예시
```python
# 좋은 예
def get_user_by_id(user_id: int) -> User:
    """사용자 ID로 사용자 조회"""
    return db.query(User).filter(User.id == user_id).first()

# 나쁜 예
def getUser(id):
    return db.query(User).filter(User.id == id).first()
```

### 파일 구조
- 각 모듈은 단일 책임을 가져야 합니다.
- 라우터는 얇게 유지하고 비즈니스 로직은 서비스 레이어에 배치합니다.
- 모델은 데이터베이스 스키마만 정의합니다.

### 에러 핸들링
- 명확한 에러 메시지 제공
- 적절한 HTTP 상태 코드 사용
- 예외는 로깅하고 사용자에게는 친화적인 메시지 표시

```python
# 좋은 예
try:
    result = await process_data(data)
except ValueError as e:
    logger.error(f"데이터 처리 실패: {e}")
    raise HTTPException(status_code=400, detail="잘못된 데이터 형식입니다.")
```

### 데이터베이스
- SQLAlchemy ORM 사용
- 트랜잭션 관리 주의
- 세션은 `get_db()` 의존성 사용
- 백그라운드 작업에서는 새로운 세션 생성

## ⚛️ TypeScript/React (Frontend) 규칙

### 코드 스타일
- **TypeScript** strict mode 사용
- **Prettier** 포맷터 사용
- **ESLint** 규칙 준수

### 네이밍 컨벤션
- **컴포넌트**: `PascalCase`
- **함수/변수**: `camelCase`
- **상수**: `UPPER_SNAKE_CASE`
- **파일명**: 컴포넌트는 `PascalCase.tsx`, 유틸은 `camelCase.ts`

### 컴포넌트 구조
```typescript
// 좋은 예
interface KeywordCardProps {
  keyword: string;
  onDelete: (id: number) => void;
}

export function KeywordCard({ keyword, onDelete }: KeywordCardProps) {
  // hooks
  const [loading, setLoading] = useState(false);
  
  // handlers
  const handleDelete = async () => {
    setLoading(true);
    await onDelete(keyword.id);
    setLoading(false);
  };
  
  // render
  return (
    <div>
      {/* JSX */}
    </div>
  );
}
```

### API 호출
- `fetch` 또는 `axios` 사용
- 에러 핸들링 필수
- 로딩 상태 관리

```typescript
// 좋은 예
async function fetchKeywords() {
  try {
    const response = await fetch('/api/keywords');
    if (!response.ok) {
      throw new Error('Failed to fetch keywords');
    }
    return await response.json();
  } catch (error) {
    console.error('Error fetching keywords:', error);
    throw error;
  }
}
```

## 🗄️ 데이터베이스 규칙

### 모델 정의
- 모든 모델은 `Base`를 상속
- 타임스탬프 필드 포함 (`created_at`, `updated_at`)
- 관계는 명시적으로 정의

### 마이그레이션
- 스키마 변경 시 마이그레이션 생성
- 마이그레이션은 되돌릴 수 있어야 함
- 프로덕션 배포 전 테스트 필수

## 🔐 보안 규칙

### 환경 변수
- 민감한 정보는 절대 코드에 하드코딩하지 않음
- `.env` 파일은 `.gitignore`에 포함
- `.env.example`에 예시만 제공

### API 키
- API 키는 환경 변수로 관리
- 키 로테이션 정책 준수
- 키 노출 시 즉시 교체

### 입력 검증
- 모든 사용자 입력 검증
- SQL 인젝션 방지 (ORM 사용)
- XSS 방지 (React는 기본적으로 처리)

## 📝 커밋 규칙

### 커밋 및 푸시 전 확인
- **중요**: 커밋 및 푸시 전에 항상 사용자에게 확인을 받아야 합니다.
- 자동으로 커밋/푸시하지 않고, 변경사항을 보여주고 승인을 받은 후 진행합니다.

### 커밋 메시지 형식
```
<type>: <subject>

<body>

<footer>
```

### Type
- `feat`: 새로운 기능
- `fix`: 버그 수정
- `docs`: 문서 수정
- `style`: 코드 포맷팅 (기능 변경 없음)
- `refactor`: 리팩토링
- `test`: 테스트 추가/수정
- `chore`: 빌드/설정 변경

### 예시
```
feat: 키워드 자동 인사이트 생성 기능 추가

- 스케줄러를 통한 주기적 인사이트 생성
- 활성화된 키워드에 대해 매일 3회 실행
- 백그라운드 작업으로 포스트 생성

Closes #123
```

## 🧪 테스트 규칙

### 테스트 작성
- 단위 테스트: 각 함수/메서드 테스트
- 통합 테스트: API 엔드포인트 테스트
- E2E 테스트: 주요 사용자 플로우 테스트

### 테스트 커버리지
- 최소 70% 이상 목표
- 핵심 비즈니스 로직은 90% 이상

## 📚 문서화 규칙

### 코드 주석
- 복잡한 로직은 주석으로 설명
- 함수/클래스는 docstring 작성
- TODO 주석은 이슈로 추적

### API 문서
- FastAPI 자동 생성 문서 활용
- 엔드포인트 설명 추가
- 요청/응답 예시 제공

### README 업데이트
- 새로운 기능 추가 시 README 업데이트
- 설치/실행 방법 변경 시 업데이트
- 환경 변수 추가 시 `.env.example` 업데이트

## 🔄 Git 워크플로우

### 브랜치 네이밍
- `feature/기능명`: 새로운 기능
- `fix/버그명`: 버그 수정
- `docs/문서명`: 문서 작업
- `refactor/리팩토링명`: 리팩토링

### Pull Request
- PR 제목은 명확하게
- 변경 사항 설명 필수
- 관련 이슈 번호 참조
- 리뷰어 지정

## 🚀 배포 규칙

### 배포 전 체크리스트
- [ ] 모든 테스트 통과
- [ ] 환경 변수 설정 확인
- [ ] 데이터베이스 마이그레이션 적용
- [ ] 로깅 설정 확인
- [ ] 모니터링 설정 확인
- [ ] 백업 계획 수립

### 버전 관리
- Semantic Versioning (MAJOR.MINOR.PATCH)
- 변경 사항은 CHANGELOG에 기록

## 📞 문의

규칙에 대한 질문이나 제안이 있으면 이슈를 생성하거나 팀에 문의하세요.


# GitHub 저장소 푸시 가이드

## 1. GitHub에서 저장소 생성

1. GitHub에 로그인: https://github.com
2. 우측 상단의 "+" 버튼 클릭 → "New repository" 선택
3. 저장소 정보 입력:
   - Repository name: `twitterautopost` (또는 원하는 이름)
   - Description: "Twitter/Instagram AI 기반 인사이트 & 포스트 생성기"
   - Public 또는 Private 선택
   - **"Initialize this repository with a README" 체크하지 않기** (이미 로컬에 있음)
4. "Create repository" 클릭

## 2. 원격 저장소 추가 및 푸시

GitHub에서 저장소를 생성한 후, 아래 명령어를 실행하세요:

```bash
# 원격 저장소 추가 (YOUR_USERNAME을 실제 GitHub 사용자명으로 변경)
git remote add origin https://github.com/YOUR_USERNAME/twitterautopost.git

# 또는 SSH 사용 시:
# git remote add origin git@github.com:YOUR_USERNAME/twitterautopost.git

# 브랜치 이름을 main으로 변경 (필요시)
git branch -M main

# GitHub에 푸시
git push -u origin main
```

## 3. 인증

GitHub에 푸시할 때 인증이 필요할 수 있습니다:
- Personal Access Token (PAT) 사용 권장
- 또는 SSH 키 설정

## 4. 확인

푸시가 완료되면 GitHub 저장소 페이지에서 파일들이 보이는지 확인하세요.


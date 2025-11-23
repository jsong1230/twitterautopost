#!/bin/bash
# GitHub 푸시 스크립트
# 사용법: ./github/PUSH_COMMANDS.sh YOUR_GITHUB_USERNAME

if [ -z "$1" ]; then
  echo "사용법: $0 YOUR_GITHUB_USERNAME"
  echo "예: $0 joohansong"
  exit 1
fi

GITHUB_USERNAME=$1
REPO_NAME="twitterautopost"

echo "원격 저장소 추가 중..."
git remote remove origin 2>/dev/null
git remote add origin "https://github.com/${GITHUB_USERNAME}/${REPO_NAME}.git"

echo "브랜치를 main으로 설정..."
git branch -M main

echo "GitHub에 푸시 중..."
echo "주의: GitHub에서 저장소를 먼저 생성해야 합니다!"
echo "저장소 URL: https://github.com/${GITHUB_USERNAME}/${REPO_NAME}"
echo ""
read -p "GitHub 저장소를 생성하셨나요? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
  git push -u origin main
else
  echo "먼저 GitHub에서 저장소를 생성해주세요."
  echo "자세한 내용은 .github/PUSH_INSTRUCTIONS.md를 참고하세요."
fi

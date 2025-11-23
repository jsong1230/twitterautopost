# 배포 및 운영 가이드

## 개발 환경 실행

### Backend 실행
```bash
cd backend
chmod +x run.sh
./run.sh
```

또는 직접:
```bash
cd backend
uvicorn main:app --reload --port 8000
```

### Frontend 실행
```bash
cd frontend
npm run dev
```

## 프로덕션 배포 (항상 켜져있는 서버)

### 방법 1: systemd 사용 (Linux)

1. 서비스 파일 수정:
```bash
sudo nano /etc/systemd/system/twitter-insights.service
```

`infra/systemd/twitter-insights.service` 파일을 참고하여 경로를 실제 경로로 수정하세요.

2. 서비스 활성화 및 시작:
```bash
sudo systemctl daemon-reload
sudo systemctl enable twitter-insights.service
sudo systemctl start twitter-insights.service
```

3. 상태 확인:
```bash
sudo systemctl status twitter-insights.service
```

### 방법 2: Supervisor 사용

1. Supervisor 설치:
```bash
sudo apt-get install supervisor  # Ubuntu/Debian
```

2. 설정 파일 복사 및 수정:
```bash
sudo cp infra/supervisor/twitter-insights.conf /etc/supervisor/conf.d/
sudo nano /etc/supervisor/conf.d/twitter-insights.conf
```

경로를 실제 경로로 수정하세요.

3. Supervisor 재시작:
```bash
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start twitter-insights-backend
```

### 방법 3: PM2 사용 (Node.js 기반 프로세스 매니저)

1. PM2 설치:
```bash
npm install -g pm2
```

2. PM2로 실행:
```bash
cd backend
pm2 start "uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4" --name twitter-insights-backend
pm2 save
pm2 startup  # 시스템 재시작 시 자동 시작 설정
```

### 방법 4: Docker 사용

Dockerfile과 docker-compose.yml을 사용하여 컨테이너로 실행할 수도 있습니다.

## 환경 변수 설정

프로덕션 환경에서는 `.env` 파일을 안전한 위치에 두고, 서비스 설정에서 환경 변수를 로드하도록 설정하세요.

## 로그 확인

- systemd: `sudo journalctl -u twitter-insights.service -f`
- Supervisor: `sudo tail -f /var/log/twitter-insights/backend.log`
- PM2: `pm2 logs twitter-insights-backend`


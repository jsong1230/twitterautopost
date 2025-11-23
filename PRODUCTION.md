# 프로덕션 배포 가이드

24시간 실행되는 프로덕션 환경 설정 가이드입니다.

## 🎯 개요

이 서비스는 **24시간 실행**되어야 합니다:
- 주기적으로 활성화된 키워드에 대해 트윗을 수집하고 인사이트를 생성합니다
- 웹 UI를 통해 언제든지 결과를 조회할 수 있어야 합니다
- 스케줄러가 매일 지정된 시간(기본: 9시, 15시, 21시)에 자동으로 실행됩니다

## 📋 사전 준비

### 1. 서버 요구사항
- Linux 서버 (Ubuntu 20.04+ 권장)
- Python 3.9 이상
- Node.js 18 이상
- 최소 2GB RAM
- 최소 10GB 디스크 공간

### 2. 환경 변수 설정

프로덕션 서버에 `.env` 파일 생성:

```bash
# 프로젝트 루트에 .env 파일 생성
nano .env
```

필수 환경 변수:
```env
# API Keys
OPENAI_API_KEY=your_openai_api_key_here
CLAUDE_API_KEY=your_claude_api_key_here
TWITTER_BEARER_TOKEN=your_twitter_bearer_token_here

# Database
DATABASE_URL=sqlite:///./twitter_insights.db

# Server
BACKEND_PORT=8000
BACKEND_HOST=0.0.0.0

# Scheduler (선택사항)
ENABLE_SCHEDULER=true
SCHEDULER_HOURS=9,15,21
```

## 🚀 배포 방법

### 방법 1: systemd 사용 (권장)

#### 1. 서비스 파일 생성

```bash
sudo nano /etc/systemd/system/twitter-insights.service
```

다음 내용 입력 (경로는 실제 경로로 수정):

```ini
[Unit]
Description=Twitter/Instagram AI 인사이트 생성기 Backend
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/path/to/twitterautopost/backend
Environment="PATH=/path/to/twitterautopost/venv/bin"
EnvironmentFile=/path/to/twitterautopost/.env
ExecStart=/path/to/twitterautopost/venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
```

#### 2. 서비스 활성화 및 시작

```bash
# 서비스 파일 리로드
sudo systemctl daemon-reload

# 서비스 활성화 (부팅 시 자동 시작)
sudo systemctl enable twitter-insights.service

# 서비스 시작
sudo systemctl start twitter-insights.service

# 상태 확인
sudo systemctl status twitter-insights.service
```

#### 3. 로그 확인

```bash
# 실시간 로그 확인
sudo journalctl -u twitter-insights.service -f

# 최근 로그 확인
sudo journalctl -u twitter-insights.service -n 100
```

### 방법 2: Supervisor 사용

#### 1. Supervisor 설치

```bash
sudo apt-get update
sudo apt-get install supervisor
```

#### 2. 설정 파일 생성

```bash
sudo nano /etc/supervisor/conf.d/twitter-insights.conf
```

다음 내용 입력:

```ini
[program:twitter-insights-backend]
command=/path/to/twitterautopost/venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
directory=/path/to/twitterautopost/backend
user=www-data
autostart=true
autorestart=true
stderr_logfile=/var/log/twitter-insights/backend_error.log
stdout_logfile=/var/log/twitter-insights/backend.log
environment=PATH="/path/to/twitterautopost/venv/bin"
environment=ENV_FILE="/path/to/twitterautopost/.env"
```

#### 3. 로그 디렉토리 생성

```bash
sudo mkdir -p /var/log/twitter-insights
sudo chown www-data:www-data /var/log/twitter-insights
```

#### 4. Supervisor 재시작

```bash
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start twitter-insights-backend
```

### 방법 3: PM2 사용 (간단한 방법)

#### 1. PM2 설치

```bash
npm install -g pm2
```

#### 2. PM2로 실행

```bash
cd /path/to/twitterautopost/backend
pm2 start "uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4" --name twitter-insights-backend
pm2 save
pm2 startup  # 시스템 재시작 시 자동 시작 설정
```

#### 3. PM2 관리

```bash
# 상태 확인
pm2 status

# 로그 확인
pm2 logs twitter-insights-backend

# 재시작
pm2 restart twitter-insights-backend

# 중지
pm2 stop twitter-insights-backend
```

## 🔧 설정 조정

### 스케줄러 시간 변경

`.env` 파일에서 `SCHEDULER_HOURS` 값을 변경:

```env
# 매 6시간마다 실행
SCHEDULER_HOURS=0,6,12,18

# 매일 오전 9시에만 실행
SCHEDULER_HOURS=9
```

### 스케줄러 비활성화

`.env` 파일에서:

```env
ENABLE_SCHEDULER=false
```

서비스 재시작 필요:
```bash
sudo systemctl restart twitter-insights.service
```

## 🔍 모니터링

### Health Check

```bash
curl http://localhost:8000/health
```

### API 문서 확인

브라우저에서 `http://your-server-ip:8000/docs` 접속

### 스케줄러 상태 확인

로그에서 스케줄러 실행 여부 확인:

```bash
# systemd
sudo journalctl -u twitter-insights.service | grep "스케줄러"

# supervisor
sudo tail -f /var/log/twitter-insights/backend.log | grep "스케줄러"

# PM2
pm2 logs twitter-insights-backend | grep "스케줄러"
```

## 🔄 업데이트 및 재시작

### 코드 업데이트 후 재시작

```bash
# systemd
sudo systemctl restart twitter-insights.service

# supervisor
sudo supervisorctl restart twitter-insights-backend

# PM2
pm2 restart twitter-insights-backend
```

### 데이터베이스 백업

```bash
# SQLite 백업
cp /path/to/twitterautopost/backend/twitter_insights.db /path/to/backup/twitter_insights_$(date +%Y%m%d).db
```

## 🛡️ 보안 고려사항

1. **방화벽 설정**: 필요한 포트만 열기
2. **HTTPS 설정**: Nginx 리버스 프록시 사용 권장
3. **API 키 보안**: `.env` 파일 권한 설정 (`chmod 600 .env`)
4. **로그 로테이션**: 로그 파일 크기 관리

## 📊 성능 최적화

### 워커 수 조정

CPU 코어 수에 맞게 워커 수 조정:

```bash
# 4코어 CPU인 경우
--workers 4

# 8코어 CPU인 경우
--workers 8
```

### 데이터베이스 최적화

SQLite는 프로덕션에서 대용량 트래픽에는 부적합할 수 있습니다. 필요시 PostgreSQL로 마이그레이션을 고려하세요.

## ❓ 문제 해결

### 서비스가 시작되지 않음

1. 로그 확인: `sudo journalctl -u twitter-insights.service -n 50`
2. 환경 변수 확인: `.env` 파일 경로 및 내용 확인
3. Python 경로 확인: 가상환경 경로가 올바른지 확인
4. 포트 확인: 다른 프로세스가 8000 포트를 사용 중인지 확인

### 스케줄러가 실행되지 않음

1. `ENABLE_SCHEDULER=true` 확인
2. 로그에서 스케줄러 시작 메시지 확인
3. 활성화된 키워드가 있는지 확인

### 메모리 부족

1. 워커 수 줄이기
2. 서버 리소스 확인
3. 로그 파일 정리

## 📞 지원

문제가 발생하면 로그를 확인하고 이슈를 생성하세요.


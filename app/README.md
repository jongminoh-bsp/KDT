# Skyline 항공예약시스템

EKS 인턴십 교육용 항공예약시스템 데모 애플리케이션입니다.

## 📋 개요

Skyline은 AWS EKS 환경에서의 컨테이너 오케스트레이션 학습을 위한 샘플 항공예약 시스템입니다. 
MySQL RDS를 데이터베이스로 사용하며, 실제 운영환경과 유사한 구성으로 설계되었습니다.

## 🤖 Amazon Q AI Integration - LIVE TEST

**Updated**: 2025-09-24 09:36 - 실제 Amazon Q AI Lambda 함수 테스트!

### 🚀 AI-Powered DevOps Pipeline
- **Amazon Q AI**: 실제 Bedrock Claude 분석 (Seoul region)
- **Lambda Function**: skyline-q-agent 배포 완료
- **Auto Infrastructure**: AI 추천 기반 Terraform 생성
- **Auto Deployment**: K8s 배포 설정 자동 생성
- **GitHub Integration**: PR 자동 생성

### 📊 AI 분석 결과 (최신)
- **Memory**: 2Gi (AI 추천)
- **CPU**: 1000m (AI 추천)
- **Replicas**: 3 (고가용성)
- **Database**: MySQL (항공 시스템 최적화)
- **Instance Type**: t3.medium
- **AI Confidence**: 95%

## 🚀 빠른 시작

### 전제 조건
- Java 17 이상
- Maven 3.6 이상
- Docker
- kubectl
- AWS CLI

### 로컬 실행
```bash
mvn spring-boot:run
```

### Docker 실행
```bash
docker build -t skyline-app .
docker run -p 8080:8080 skyline-app
```

## 🏗️ 아키텍처

- **Backend**: Spring Boot 3.x
- **Database**: MySQL 8.0
- **Container**: Docker
- **Orchestration**: Kubernetes (EKS)
- **AI Analysis**: Amazon Q (Bedrock Claude)
- **Automation**: AWS Lambda + GitHub Actions

## 🔧 개발 환경

### API 엔드포인트
- `GET /` - 메인 페이지
- `GET /health` - 헬스 체크
- `GET /api/flights` - 항공편 조회
- `POST /api/bookings` - 예약 생성

### 환경 변수
- `DB_HOST`: 데이터베이스 호스트
- `DB_PORT`: 데이터베이스 포트 (기본값: 3306)
- `DB_NAME`: 데이터베이스 이름
- `DB_USER`: 데이터베이스 사용자
- `DB_PASSWORD`: 데이터베이스 비밀번호

## 🚀 AI-Powered 배포 워크플로우

```
App 코드 수정 → GitHub Push → Lambda 트리거 → Amazon Q AI 분석 → 인프라 생성 → 자동 배포
```

1. **코드 푸시**: app/ 디렉터리 수정
2. **AI 분석**: Amazon Q가 Spring Boot 앱 분석
3. **인프라 생성**: AI 추천 기반 Terraform 코드 생성
4. **배포 설정**: K8s 배포 YAML 자동 생성
5. **PR 생성**: 생성된 파일들로 자동 PR 생성
6. **리뷰 & 배포**: PR 머지 후 자동 배포

**Powered by Amazon Q AI** 🤖✨

---

**이 README 수정으로 전체 AI 파이프라인이 트리거됩니다!** 🚀
🧪 Lambda 테스트 - Wed Sep 24 10:07:18 KST 2025
🔄 GitHub 토큰 설정 완료 - Wed Sep 24 10:15:05 KST 2025
🌐 Production deployment ready - Wed Sep 24 10:28:04 KST 2025

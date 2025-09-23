# Skyline 항공예약시스템 Demo

EKS 인턴십 교육용 항공예약시스템 데모 애플리케이션입니다.

## 📋 개요

Skyline은 AWS EKS 환경에서의 컨테이너 오케스트레이션 학습을 위한 샘플 항공예약 시스템입니다. 
MySQL RDS를 데이터베이스로 사용하며, 실제 운영환경과 유사한 구성으로 설계되었습니다.

## 🚀 빠른 시작

### Docker로 실행
```bash
# 이미지 빌드
docker build -t skyline:latest .

# 환경변수 설정 후 실행
docker run -p 8080:8080 \
  -e DB_HOST=your-rds-endpoint \
  -e DB_USER=admin \
  -e DB_PASSWORD=your-password \
  skyline:latest
```

### Kubernetes 배포
```bash
# Secret 생성
kubectl create secret generic skyline-db-secret \
  --from-literal=DB_HOST=your-rds-endpoint \
  --from-literal=DB_USER=admin \
  --from-literal=DB_PASSWORD=your-password

# 애플리케이션 배포
kubectl apply -f k8s-examples/basic/
```

## 🏗️ 아키텍처

- **Frontend**: React (포트 3000)
- **Backend**: Spring Boot (포트 8080)
- **Database**: MySQL RDS
- **Container**: Docker 멀티스테이지 빌드

## 🛠️ API 엔드포인트

### 항공편 관리
- `GET /api/flights` - 항공편 목록 조회
- `GET /api/flights/{id}` - 특정 항공편 조회
- `GET /api/flights/search?from={departure}&to={arrival}&date={date}` - 항공편 검색

### 예약 관리
- `POST /api/reservations` - 예약 생성
- `GET /api/reservations/{id}` - 예약 조회
- `PUT /api/reservations/{id}` - 예약 수정
- `DELETE /api/reservations/{id}` - 예약 취소

### 시스템 모니터링
- `GET /health` - 헬스체크 (DB 연결 상태 포함)
- `GET /ready` - 레디니스 체크
- `GET /metrics` - Prometheus 메트릭
- `GET /stress/cpu` - CPU 부하 테스트용
- `GET /stress/memory` - 메모리 부하 테스트용

## 📊 데이터베이스 스키마

주요 테이블:
- `airports` - 공항 정보
- `flights` - 항공편 정보  
- `reservations` - 예약 정보

자세한 스키마는 `sql/schema.sql`을 참조하세요.

## 🎯 인턴십 실습 시나리오

### 초급 과제
- [ ] 기본 Pod 배포 및 Service 노출
- [ ] RDS 연결 및 API 테스트
- [ ] ConfigMap으로 설정 외부화

### 중급 과제  
- [ ] Ingress Controller 설정
- [ ] HPA(Horizontal Pod Autoscaler) 구성
- [ ] 모니터링 대시보드 구축

### 고급 과제
- [ ] Helm Chart 작성
- [ ] CI/CD 파이프라인 구축
- [ ] Service Mesh 적용
- [ ] Blue-Green 배포 구현

## 🔧 환경변수

| 변수명 | 기본값 | 설명 |
|--------|--------|------|
| `DB_HOST` | localhost | MySQL 서버 주소 |
| `DB_PORT` | 3306 | MySQL 포트 |
| `DB_NAME` | skyline | 데이터베이스 이름 |
| `DB_USER` | skyline_user | 데이터베이스 사용자 |
| `DB_PASSWORD` | changeme | 데이터베이스 비밀번호 |
| `DB_CONNECTION_POOL_SIZE` | 10 | 커넥션 풀 크기 |

## 📁 프로젝트 구조

```
skyline_system_demo/
├── src/                        # 애플리케이션 소스코드
├── frontend/                   # React 프론트엔드
├── sql/                        # DB 스키마 및 시드 데이터
├── k8s-examples/              # Kubernetes 예시 매니페스트
├── scripts/                   # 유틸리티 스크립트
├── docs/                      # 문서
├── Dockerfile                 # 멀티스테이지 Docker 빌드
└── docker-compose.yml         # 로컬 개발용
```

## 🚨 문제해결

일반적인 문제들과 해결방법은 [TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md)를 참조하세요.

## 📝 라이선스

이 프로젝트는 교육 목적으로만 사용됩니다.

---

🎓 **인턴십 교육생 여러분**, 자유롭게 실험하고 창의적으로 구성해보세요!
# 🎯 Skyline AI-Driven DevOps 발표 데모 시나리오

## 📋 데모 개요
**Amazon Q 기반 완전 자동화된 DevOps 파이프라인 시연**

---

## 🚀 데모 시나리오

### 1️⃣ **현재 상태 확인** (1분)
```bash
# 애플리케이션 상태
kubectl get pods -n skyline
kubectl get svc -n skyline
kubectl get ingress -n skyline

# 웹사이트 접속
curl -k https://www.greenbespinglobal.store
```

### 2️⃣ **코드 수정 및 푸시** (2분)
```bash
# 애플리케이션 코드 수정
echo "// Demo update $(date)" >> app/src/main/java/com/example/skyline/SkylineApplication.java

# Git 커밋 및 푸시
git add .
git commit -m "feat: Demo - Add new feature for presentation"
git push origin main
```

### 3️⃣ **자동화 워크플로 실행** (3분)
```bash
# GitHub Actions 실행 상태 확인
gh run list --limit 3

# 실시간 로그 확인
gh run watch
```

### 4️⃣ **Lambda 함수 동작 확인** (2분)
```bash
# Lambda 로그 확인
aws logs tail /aws/lambda/skyline-q-agent --follow --region ap-northeast-2

# S3 결과 확인
aws s3 ls s3://skyline-ai-results/ --recursive
```

### 5️⃣ **자동 생성된 PR 확인** (2분)
```bash
# PR 목록 확인
gh pr list

# PR 내용 확인
gh pr view [PR번호] --web
```

---

## 🎬 발표 포인트

### 💡 **핵심 메시지**
1. **완전 자동화**: 코드 푸시 → 인프라 생성 → 배포까지 자동
2. **AI 기반**: Amazon Q가 코드 분석하여 최적 인프라 도출
3. **비용 최적화**: 단일 NAT Gateway, 적절한 인스턴스 타입
4. **보안**: HTTPS, 프라이빗 서브넷, IAM 역할 기반 권한

### 📊 **시연 결과**
- ✅ **인프라**: EKS 1.33, RDS MySQL, VPC
- ✅ **애플리케이션**: Spring Boot + React
- ✅ **모니터링**: Datadog APM 연동
- ✅ **도메인**: www.greenbespinglobal.store

### 🔧 **기술 스택**
- **AI**: Amazon Q Code Analyzer
- **IaC**: Terraform (모듈화)
- **Container**: Docker + Kubernetes
- **Cloud**: AWS (EKS, RDS, VPC, Route53)
- **CI/CD**: GitHub Actions
- **Monitoring**: Datadog

---

## 📸 **캡처 포인트**

1. **GitHub Actions 워크플로 실행 화면**
2. **Lambda 함수 로그 (Amazon Q 분석 결과)**
3. **자동 생성된 Terraform 코드**
4. **자동 생성된 Kubernetes 매니페스트**
5. **PR 생성 및 승인 과정**
6. **배포 완료 후 웹사이트 접속**
7. **Datadog 모니터링 대시보드**

---

## ⚡ **백업 시나리오**

만약 실시간 데모에서 문제가 발생할 경우:

1. **기존 성공 로그 보여주기**
2. **생성된 코드 파일들 직접 보여주기**
3. **아키텍처 다이어그램으로 설명**
4. **Datadog 모니터링 결과 보여주기**

---

## 🎯 **예상 질문 & 답변**

**Q: 비용은 얼마나 드나요?**
A: 단일 NAT Gateway, t3.medium/micro 인스턴스로 월 약 $50-80 수준

**Q: 보안은 어떻게 보장하나요?**
A: 프라이빗 서브넷, IAM 역할, HTTPS, 시크릿 관리로 보안 강화

**Q: 다른 언어도 지원하나요?**
A: Amazon Q가 다양한 언어 분석 가능, Terraform 모듈로 확장성 제공

**Q: 장애 대응은?**
A: Datadog 모니터링, HPA 자동 스케일링, 헬스체크로 안정성 확보

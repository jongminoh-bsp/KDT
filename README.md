# KDT - AI-Driven DevOps Automation Platform

## 🎯 프로젝트 개요

Amazon Q 기반 완전 자동화된 DevOps 파이프라인 구축 프로젝트

### 🚀 핵심 기능

1. **AI 코드 분석**: 애플리케이션 코드 자동 분석 및 인프라 요구사항 도출
2. **동적 인프라 생성**: Terraform 코드 자동 생성 및 AWS 리소스 배포
3. **K8s 자동 배포**: Kubernetes 매니페스트 생성 및 애플리케이션 배포
4. **도메인 연결**: HTTPS 인증서 및 도메인 자동 설정

### 🌿 브랜치 전략

- `main`: 프로덕션 환경
- `stag`: 스테이징 환경  
- `dev`: 개발 환경

### 📋 워크플로우

```
개발자 코드 푸시 → Amazon Q 분석 → Terraform 생성 → PR → 인프라 배포 → K8s 배포 → 도메인 연결
```

## 🛠️ 기술 스택

- **AI**: Amazon Q Code Analyzer
- **IaC**: Terraform (모듈화)
- **Container**: Docker + Kubernetes
- **Cloud**: AWS (EKS, RDS, VPC, Route53)
- **CI/CD**: GitHub Actions

---

**Status**: 🚧 개발 중 - AI 코드 분석 엔진 완료

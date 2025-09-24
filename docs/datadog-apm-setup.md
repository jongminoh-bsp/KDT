# Datadog APM 설정 가이드

## 📋 개요

KDT Skyline 프로젝트에서 Datadog APM(Application Performance Monitoring)을 구축하여 애플리케이션 성능 모니터링을 구현한 가이드입니다.

## 🎯 구축 목표

- Java Spring Boot 애플리케이션 성능 모니터링
- 실시간 트레이스 및 메트릭 수집
- 로그와 트레이스 상관관계 분석
- 자동화된 APM 라이브러리 주입

## 🛠️ 구축 아키텍처

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Skyline App   │───▶│  Datadog Agent   │───▶│ Datadog Cloud   │
│  (Java + APM)   │    │   (DaemonSet)    │    │   Dashboard     │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                       │
         │              ┌────────▼────────┐
         └─────────────▶│ Admission       │
                        │ Controller      │
                        └─────────────────┘
```

## 📦 설치 구성요소

### 1. Datadog Operator
- **역할**: Kubernetes 환경에서 Datadog 리소스 관리
- **네임스페이스**: `datadog`

### 2. Datadog Agent
- **배포 방식**: DaemonSet (각 노드에 1개씩)
- **기능**: APM 트레이스 수집, 로그 수집, 메트릭 수집

### 3. Admission Controller
- **역할**: Pod 생성 시 APM 라이브러리 자동 주입
- **웹훅**: `datadog-webhook`

## 🚀 설치 과정

### 1단계: Datadog Operator 설치

```bash
# 네임스페이스 생성
kubectl create namespace datadog

# Helm 리포지토리 추가
helm repo add datadog https://helm.datadoghq.com --insecure-skip-tls-verify
helm repo update

# Datadog Operator 설치
helm install datadog-operator datadog/datadog-operator -n datadog
```

### 2단계: API 키 설정

```bash
# Datadog API 키 시크릿 생성
kubectl create secret generic datadog-secret \
  --from-literal api-key=<YOUR_DATADOG_API_KEY> \
  -n datadog
```

### 3단계: Datadog Agent 배포

```yaml
# datadog-agent.yaml
apiVersion: datadoghq.com/v2alpha1
kind: DatadogAgent
metadata:
  name: datadog
  namespace: datadog
spec:
  global:
    site: datadoghq.com
    credentials:
      apiSecret:
        secretName: datadog-secret
        keyName: api-key
  features:
    apm:
      enabled: true
      hostPortConfig:
        enabled: true
        hostPort: 8126
    logCollection:
      enabled: true
    liveProcessCollection:
      enabled: true
    admissionController:
      enabled: true
      mutateUnlabelled: false
  override:
    nodeAgent:
      env:
        - name: DD_APM_ENABLED
          value: "true"
        - name: DD_APM_NON_LOCAL_TRAFFIC
          value: "true"
        - name: DD_LOGS_ENABLED
          value: "true"
        - name: DD_LOGS_CONFIG_CONTAINER_COLLECT_ALL
          value: "true"
```

```bash
kubectl apply -f datadog-agent.yaml
```

### 4단계: 애플리케이션 APM 설정

```yaml
# skyline-app APM 설정
apiVersion: apps/v1
kind: Deployment
metadata:
  name: skyline-app
  namespace: skyline
  labels:
    tags.datadoghq.com/env: dev
    tags.datadoghq.com/service: skyline-app
    tags.datadoghq.com/version: v1.0.0
spec:
  template:
    metadata:
      labels:
        tags.datadoghq.com/env: dev
        tags.datadoghq.com/service: skyline-app
        tags.datadoghq.com/version: v1.0.0
        admission.datadoghq.com/enabled: "true"
      annotations:
        admission.datadoghq.com/java-lib.version: v1.53.0
    spec:
      containers:
      - name: skyline
        env:
        - name: DD_SERVICE
          value: skyline-app
        - name: DD_ENV
          value: dev
        - name: DD_VERSION
          value: v1.0.0
        - name: DD_LOGS_INJECTION
          value: "true"
```

## 🔍 설치 확인

### 1. Datadog 구성요소 상태 확인
```bash
# Operator 상태
kubectl get pods -n datadog

# Admission Controller 웹훅 확인
kubectl get mutatingwebhookconfigurations | grep datadog
```

### 2. APM 라이브러리 주입 확인
```bash
# 애플리케이션 재시작
kubectl rollout restart deployment/skyline-app -n skyline

# APM 에이전트 로드 확인
kubectl logs <pod-name> -n skyline | grep "DATADOG TRACER"
```

### 3. 예상 출력
```
Picked up JAVA_TOOL_OPTIONS: -javaagent:/opt/datadog/apm/library/java/dd-java-agent.jar
[dd.trace] INFO datadog.trace.agent.core.StatusLogger - DATADOG TRACER CONFIGURATION
```

## 📊 Datadog 대시보드 접근

### APM 서비스 확인
1. **Datadog 콘솔** → **APM** → **Services**
2. `skyline-app` 서비스 클릭
3. 성능 메트릭 확인:
   - 응답 시간 (Latency)
   - 처리량 (Throughput)  
   - 에러율 (Error Rate)
   - Apdex 점수

### 주요 모니터링 메트릭
- `trace.servlet.request.duration`: 요청 응답 시간
- `trace.servlet.request.hits`: 요청 수
- `trace.servlet.request.errors`: 에러 수
- `jvm.heap_memory`: JVM 힙 메모리
- `jvm.cpu_load.process`: JVM CPU 사용률

## 🚨 트러블슈팅

### 문제 1: APM 데이터가 보이지 않음
**해결책:**
```bash
# Admission Controller 확인
kubectl get mutatingwebhookconfigurations

# Pod 재시작으로 라이브러리 재주입
kubectl rollout restart deployment/skyline-app -n skyline
```

### 문제 2: Agent 연결 실패
**해결책:**
```bash
# Agent 상태 확인
kubectl get pods -n datadog
kubectl logs datadog-agent-<pod-id> -n datadog

# API 키 확인
kubectl get secret datadog-secret -n datadog -o yaml
```

## 📈 성능 최적화 팁

1. **샘플링 설정**: 높은 트래픽 환경에서 샘플링 비율 조정
2. **태그 전략**: 일관된 태그 사용으로 메트릭 그룹화
3. **알림 설정**: 임계값 기반 성능 알림 구성
4. **로그 상관관계**: `DD_LOGS_INJECTION=true`로 트레이스-로그 연결

## 🔗 관련 파일

- `datadog-agent.yaml`: Datadog Agent 설정
- `skyline-app-apm.yaml`: APM이 적용된 애플리케이션 배포 설정

---

**구축 완료일**: 2025-09-24  
**담당자**: KDT 프로젝트 팀  
**Datadog 버전**: Agent v7.x, Java APM v1.53.0

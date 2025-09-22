# KDT 프로젝트 구조

## 📁 디렉터리 구조

```
KDT/
├── automation/                 # AI 자동화 엔진
│   ├── analyzer/              # 코드 분석기
│   │   └── code_analyzer.py   # Amazon Q 코드 분석 엔진
│   ├── generator/             # Terraform 코드 생성기
│   └── templates/             # 템플릿 파일들
├── terraform/                 # 인프라 코드
│   ├── modules/               # 재사용 가능한 모듈
│   └── environments/          # 환경별 설정
├── k8s/                       # Kubernetes 매니페스트
│   ├── base/                  # 기본 설정
│   └── overlays/              # 환경별 오버레이
├── docs/                      # 문서
├── tests/                     # 테스트 코드
└── README.md                  # 프로젝트 개요
```

## 🌿 브랜치 전략

### main
- 프로덕션 환경 배포용
- 안정적이고 테스트된 코드만 포함
- 직접 커밋 금지, PR을 통해서만 머지

### stag  
- 스테이징 환경 테스트용
- 프로덕션 배포 전 최종 검증
- dev에서만 머지 허용

### dev
- 개발 통합 환경
- 기능 브랜치들의 통합 지점
- 개발팀 공유 브랜치

## 🔄 개발 워크플로우

1. `dev`에서 기능 브랜치 생성
2. 기능 개발 및 테스트
3. `dev`로 PR 생성
4. 코드 리뷰 및 승인
5. `dev` → `stag` → `main` 순서로 배포

## 🎯 핵심 컴포넌트

### 1. Amazon Q Code Analyzer
- 애플리케이션 코드 자동 분석
- 인프라 요구사항 도출
- 리소스 최적화 추천

### 2. Terraform Generator  
- 분석 결과 기반 인프라 코드 생성
- 모듈화된 구조
- 환경별 설정 지원

### 3. K8s Manifest Generator
- 애플리케이션별 최적화된 매니페스트
- 자동 스케일링 설정
- 보안 정책 적용

### 4. GitHub Actions Pipeline
- 자동 빌드 및 배포
- 단계별 승인 프로세스
- 롤백 지원

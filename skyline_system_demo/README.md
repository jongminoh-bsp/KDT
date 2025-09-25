# Skyline System Demo

이 디렉토리의 변경사항이 git에 푸시되면 자동으로 Terraform과 K8s 코드가 생성되어 배포됩니다.

## 자동화 프로세스

1. `skyline_system_demo/` 변경 감지
2. 기존 `/home/ojm/KDT/terraform` 코드 기반으로 인프라 코드 생성
3. K8s 매니페스트 자동 생성
4. 기존 `skyline-dev-cluster`에 배포

## 배포 대상

- **EKS**: skyline-dev-cluster
- **RDS**: skyline-dev-db
- **도메인**: www.greenbespinglobal.store

## 트리거 방법

```bash
# 파일 수정 후
git add skyline_system_demo/
git commit -m "Update demo app"
git push origin main
```

#!/bin/bash

echo "🚀 APM 이미지 빌드 시작..."

# ECR 로그인
aws ecr get-login-password --region ap-northeast-2 | docker login --username AWS --password-stdin 646558765106.dkr.ecr.ap-northeast-2.amazonaws.com

# ECR 레포지토리 생성 (이미 있으면 무시)
aws ecr create-repository --repository-name skyline-app-apm --region ap-northeast-2 || true

# APM 이미지 빌드
cd /home/ojm/KDT/app
docker build -f Dockerfile.apm -t skyline-app-apm:latest .

# ECR에 태그 및 푸시
docker tag skyline-app-apm:latest 646558765106.dkr.ecr.ap-northeast-2.amazonaws.com/skyline-app-apm:latest
docker push 646558765106.dkr.ecr.ap-northeast-2.amazonaws.com/skyline-app-apm:latest

echo "✅ APM 이미지 빌드 완료!"

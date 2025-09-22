#!/usr/bin/env python3
"""
KDT 프로젝트 설정 파일
"""

# 애플리케이션 분석 대상 경로
APPLICATION_SOURCE_PATH = "/home/ojm/KDT/app"

# ECR 이미지 설정
ECR_REGISTRY = "646558765106.dkr.ecr.ap-northeast-2.amazonaws.com"
ECR_REPOSITORY = "skyline-dev"
ECR_TAG = "latest"
ECR_IMAGE_URI = f"{ECR_REGISTRY}/{ECR_REPOSITORY}:{ECR_TAG}"

# AWS 설정
AWS_REGION = "ap-northeast-2"
AWS_ACCOUNT_ID = "646558765106"

# 도메인 설정
DOMAIN_NAME = "www.greenbespinglobal.store"
SSL_CERTIFICATE_ARN = "arn:aws:acm:ap-northeast-2:646558765106:certificate/a6b78edc-d61d-4e6c-9aa5-d2344870e68e"

# 프로젝트 설정
PROJECT_NAME = "skyline"
ENVIRONMENT = "dev"

# Kubernetes 설정
K8S_NAMESPACE = "skyline"
K8S_SERVICE_NAME = "skyline-service"
K8S_DEPLOYMENT_NAME = "skyline-app"

print(f"📋 Configuration loaded:")
print(f"   Application Path: {APPLICATION_SOURCE_PATH}")
print(f"   ECR Image: {ECR_IMAGE_URI}")
print(f"   Domain: {DOMAIN_NAME}")
print(f"   Environment: {ENVIRONMENT}")

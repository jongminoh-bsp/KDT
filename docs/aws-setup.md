# AWS 설정 가이드

## 🔑 GitHub Actions용 AWS IAM 역할 설정

GitHub Actions에서 Terraform을 실행하기 위한 AWS 권한 설정 방법입니다.

### 1. IAM 역할 생성

```bash
# IAM 역할 생성
aws iam create-role \
  --role-name GitHubActions-TerraformDeploy \
  --assume-role-policy-document '{
    "Version": "2012-10-17",
    "Statement": [
      {
        "Effect": "Allow",
        "Principal": {
          "Federated": "arn:aws:iam::646558765106:oidc-provider/token.actions.githubusercontent.com"
        },
        "Action": "sts:AssumeRole",
        "Condition": {
          "StringEquals": {
            "token.actions.githubusercontent.com:aud": "sts.amazonaws.com",
            "token.actions.githubusercontent.com:sub": "repo:jongminoh-bsp/KDT:ref:refs/heads/dev"
          }
        }
      }
    ]
  }'
```

### 2. 필요한 권한 정책 연결

```bash
# EC2 전체 권한
aws iam attach-role-policy \
  --role-name GitHubActions-TerraformDeploy \
  --policy-arn arn:aws:iam::aws:policy/AmazonEC2FullAccess

# EKS 전체 권한  
aws iam attach-role-policy \
  --role-name GitHubActions-TerraformDeploy \
  --policy-arn arn:aws:iam::aws:policy/AmazonEKSClusterPolicy

# RDS 전체 권한
aws iam attach-role-policy \
  --role-name GitHubActions-TerraformDeploy \
  --policy-arn arn:aws:iam::aws:policy/AmazonRDSFullAccess

# IAM 권한 (역할 생성용)
aws iam attach-role-policy \
  --role-name GitHubActions-TerraformDeploy \
  --policy-arn arn:aws:iam::aws:policy/IAMFullAccess

# VPC 권한
aws iam attach-role-policy \
  --role-name GitHubActions-TerraformDeploy \
  --policy-arn arn:aws:iam::aws:policy/AmazonVPCFullAccess
```

### 3. GitHub Secrets 설정

GitHub 저장소의 Settings > Secrets and variables > Actions에서 다음 시크릿을 추가:

```
AWS_ROLE_ARN = arn:aws:iam::646558765106:role/GitHubActions-TerraformDeploy
```

### 4. OIDC Provider 설정 (한 번만 실행)

```bash
# GitHub Actions OIDC Provider 생성
aws iam create-open-id-connect-provider \
  --url https://token.actions.githubusercontent.com \
  --client-id-list sts.amazonaws.com \
  --thumbprint-list 6938fd4d98bab03faadb97b34396831e3780aea1
```

## 🔧 Terraform Backend 설정 (선택사항)

S3 백엔드를 사용하려면:

### 1. S3 버킷 생성

```bash
aws s3 mb s3://kdt-terraform-state-646558765106 --region ap-northeast-2
```

### 2. DynamoDB 테이블 생성 (상태 잠금용)

```bash
aws dynamodb create-table \
  --table-name kdt-terraform-locks \
  --attribute-definitions AttributeName=LockID,AttributeType=S \
  --key-schema AttributeName=LockID,KeyType=HASH \
  --provisioned-throughput ReadCapacityUnits=5,WriteCapacityUnits=5 \
  --region ap-northeast-2
```

### 3. Terraform 백엔드 설정

`terraform/backend.tf` 파일 생성:

```hcl
terraform {
  backend "s3" {
    bucket         = "kdt-terraform-state-646558765106"
    key            = "infrastructure/terraform.tfstate"
    region         = "ap-northeast-2"
    dynamodb_table = "kdt-terraform-locks"
    encrypt        = true
  }
}
```

## ✅ 설정 확인

```bash
# IAM 역할 확인
aws iam get-role --role-name GitHubActions-TerraformDeploy

# 연결된 정책 확인
aws iam list-attached-role-policies --role-name GitHubActions-TerraformDeploy

# OIDC Provider 확인
aws iam list-open-id-connect-providers
```

이제 GitHub Actions에서 AWS 리소스를 안전하게 관리할 수 있습니다! 🚀

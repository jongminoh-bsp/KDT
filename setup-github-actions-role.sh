#!/bin/bash
# GitHub Actions용 완전한 AWS 역할 설정

echo "🔧 Setting up complete GitHub Actions AWS role..."

# 1. OIDC Provider 생성 (이미 있으면 스킵)
echo "📋 Creating GitHub OIDC Provider..."
aws iam create-open-id-connect-provider \
  --url https://token.actions.githubusercontent.com \
  --client-id-list sts.amazonaws.com \
  --thumbprint-list 6938fd4d98bab03faadb97b34396831e3780aea1 \
  2>/dev/null || echo "OIDC Provider already exists"

# 2. GitHub Actions 역할 생성
echo "🔑 Creating GitHub Actions role..."
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
            "token.actions.githubusercontent.com:aud": "sts.amazonaws.com"
          },
          "StringLike": {
            "token.actions.githubusercontent.com:sub": "repo:jongminoh-bsp/KDT:*"
          }
        }
      }
    ]
  }'

# 3. 필요한 권한들 연결
echo "🔗 Attaching policies..."

# EC2 권한
aws iam attach-role-policy \
  --role-name GitHubActions-TerraformDeploy \
  --policy-arn arn:aws:iam::aws:policy/AmazonEC2FullAccess

# EKS 권한
aws iam attach-role-policy \
  --role-name GitHubActions-TerraformDeploy \
  --policy-arn arn:aws:iam::aws:policy/AmazonEKSClusterPolicy

# RDS 권한
aws iam attach-role-policy \
  --role-name GitHubActions-TerraformDeploy \
  --policy-arn arn:aws:iam::aws:policy/AmazonRDSFullAccess

# IAM 권한
aws iam attach-role-policy \
  --role-name GitHubActions-TerraformDeploy \
  --policy-arn arn:aws:iam::aws:policy/IAMFullAccess

# VPC 권한
aws iam attach-role-policy \
  --role-name GitHubActions-TerraformDeploy \
  --policy-arn arn:aws:iam::aws:policy/AmazonVPCFullAccess

# 4. Bedrock 권한 연결
echo "🤖 Attaching Bedrock permissions..."
aws iam attach-role-policy \
  --role-name GitHubActions-TerraformDeploy \
  --policy-arn arn:aws:iam::646558765106:policy/GitHubActions-BedrockAccess

# 5. 역할 ARN 출력
echo ""
echo "✅ GitHub Actions role setup complete!"
echo ""
echo "🔑 Role ARN (add this to GitHub Secrets as AWS_ROLE_ARN):"
aws iam get-role --role-name GitHubActions-TerraformDeploy --query 'Role.Arn' --output text

echo ""
echo "📋 Next steps:"
echo "1. Copy the Role ARN above"
echo "2. Go to GitHub repo Settings > Secrets and variables > Actions"
echo "3. Add new secret: AWS_ROLE_ARN = <the ARN above>"
echo "4. Enable Claude model access in AWS Bedrock console"

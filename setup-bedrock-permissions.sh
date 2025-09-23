#!/bin/bash
# AWS Bedrock 권한 설정 스크립트

echo "🔧 Setting up AWS Bedrock permissions for GitHub Actions..."

# 1. Bedrock 권한 정책 생성
echo "📋 Creating Bedrock policy..."
aws iam create-policy \
  --policy-name GitHubActions-BedrockAccess \
  --policy-document '{
    "Version": "2012-10-17",
    "Statement": [
      {
        "Effect": "Allow",
        "Action": [
          "bedrock:InvokeModel",
          "bedrock:InvokeModelWithResponseStream",
          "bedrock:ListFoundationModels",
          "bedrock:GetFoundationModel"
        ],
        "Resource": "*"
      }
    ]
  }' \
  --description "Bedrock access for GitHub Actions"

# 2. 기존 GitHub Actions 역할에 Bedrock 정책 연결
echo "🔗 Attaching Bedrock policy to existing role..."
aws iam attach-role-policy \
  --role-name GitHubActions-TerraformDeploy \
  --policy-arn arn:aws:iam::646558765106:policy/GitHubActions-BedrockAccess

# 3. 역할 확인
echo "✅ Checking role policies..."
aws iam list-attached-role-policies --role-name GitHubActions-TerraformDeploy

echo "🎉 Bedrock permissions setup complete!"
echo ""
echo "📋 Next steps:"
echo "1. Enable Claude model access in AWS Bedrock console"
echo "2. Verify GitHub secret AWS_ROLE_ARN is set"
echo "3. Test the workflow"

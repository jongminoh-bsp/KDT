#!/bin/bash

echo "🚀 Setting up Amazon Q Agent Lambda with GitHub Integration"
echo "=========================================================="

# Variables
FUNCTION_NAME="skyline-q-agent"
REGION="ap-northeast-2"
ROLE_NAME="SkylineQAgentRole"
BUCKET_NAME="skyline-ai-results"

# Get GitHub token
read -p "Enter GitHub Personal Access Token: " GITHUB_TOKEN

echo "📦 Creating S3 bucket..."
aws s3 mb s3://$BUCKET_NAME --region $REGION 2>/dev/null || echo "Bucket exists"

echo "📦 Creating Lambda package..."
cd aws-lambda
pip install requests -t .
zip -r skyline-q-agent.zip . -x "*.pyc" "__pycache__/*"

echo "🔑 Creating IAM role..."
aws iam create-role \
    --role-name $ROLE_NAME \
    --assume-role-policy-document '{
        "Version": "2012-10-17",
        "Statement": [{
            "Effect": "Allow",
            "Principal": {"Service": "lambda.amazonaws.com"},
            "Action": "sts:AssumeRole"
        }]
    }' 2>/dev/null || echo "Role exists"

echo "📋 Attaching policies..."
aws iam attach-role-policy --role-name $ROLE_NAME --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole
aws iam attach-role-policy --role-name $ROLE_NAME --policy-arn arn:aws:iam::aws:policy/AmazonBedrockFullAccess
aws iam attach-role-policy --role-name $ROLE_NAME --policy-arn arn:aws:iam::aws:policy/AmazonS3FullAccess

sleep 10

echo "🤖 Creating Lambda function..."
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
ROLE_ARN="arn:aws:iam::${ACCOUNT_ID}:role/${ROLE_NAME}"

aws lambda create-function \
    --function-name $FUNCTION_NAME \
    --runtime python3.11 \
    --role $ROLE_ARN \
    --handler skyline-q-agent.lambda_handler \
    --zip-file fileb://skyline-q-agent.zip \
    --timeout 300 \
    --memory-size 1024 \
    --region $REGION 2>/dev/null || \
aws lambda update-function-code \
    --function-name $FUNCTION_NAME \
    --zip-file fileb://skyline-q-agent.zip

echo "⚙️ Setting environment variables..."
aws lambda update-function-configuration \
    --function-name $FUNCTION_NAME \
    --environment Variables='{
        "AWS_DEFAULT_REGION":"ap-northeast-2",
        "GITHUB_TOKEN":"'$GITHUB_TOKEN'",
        "S3_BUCKET":"'$BUCKET_NAME'"
    }'

echo "✅ Setup completed!"
echo ""
echo "🎯 Complete workflow:"
echo "1. App code push → GitHub Actions triggers Lambda"
echo "2. Lambda runs Amazon Q AI analysis"
echo "3. Lambda generates Terraform & K8s configs"
echo "4. Lambda creates GitHub PR with generated files"
echo "5. Review and merge PR to deploy!"
echo ""
echo "🧪 Test:"
echo "aws lambda invoke --function-name $FUNCTION_NAME --payload '{\"repository\":\"KDT\",\"branch\":\"dev\"}' response.json"

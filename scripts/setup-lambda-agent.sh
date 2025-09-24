#!/bin/bash

echo "🚀 Setting up Amazon Q Agent Lambda Function (Serverless)"
echo "========================================================"

# Variables
FUNCTION_NAME="skyline-q-agent"
REGION="ap-northeast-2"
ROLE_NAME="SkylineQAgentRole"
BUCKET_NAME="skyline-ai-results"

echo "📦 Creating S3 bucket for results..."
aws s3 mb s3://$BUCKET_NAME --region $REGION 2>/dev/null || echo "Bucket already exists"

echo "📦 Creating Lambda deployment package..."
cd aws-lambda
zip -r skyline-q-agent.zip skyline-q-agent.py

echo "🔑 Creating IAM role for Lambda..."
aws iam create-role \
    --role-name $ROLE_NAME \
    --assume-role-policy-document '{
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": {
                    "Service": "lambda.amazonaws.com"
                },
                "Action": "sts:AssumeRole"
            }
        ]
    }' \
    --region $REGION 2>/dev/null || echo "Role already exists"

echo "📋 Attaching policies to role..."
aws iam attach-role-policy \
    --role-name $ROLE_NAME \
    --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole

aws iam attach-role-policy \
    --role-name $ROLE_NAME \
    --policy-arn arn:aws:iam::aws:policy/AmazonBedrockFullAccess

aws iam attach-role-policy \
    --role-name $ROLE_NAME \
    --policy-arn arn:aws:iam::aws:policy/AmazonS3FullAccess

echo "⏳ Waiting for role to be ready..."
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
    --memory-size 512 \
    --region $REGION \
    --description "Amazon Q Agent for Skyline app analysis (Serverless)" 2>/dev/null || \
aws lambda update-function-code \
    --function-name $FUNCTION_NAME \
    --zip-file fileb://skyline-q-agent.zip \
    --region $REGION

echo "⚙️ Configuring Lambda environment..."
aws lambda update-function-configuration \
    --function-name $FUNCTION_NAME \
    --environment Variables='{
        "AWS_DEFAULT_REGION":"ap-northeast-2",
        "BEDROCK_REGION":"ap-northeast-2",
        "S3_BUCKET":"'$BUCKET_NAME'"
    }' \
    --region $REGION

echo "✅ Amazon Q Agent Lambda setup completed!"
echo ""
echo "🎯 Architecture:"
echo "- No EC2 instances needed"
echo "- Lambda processes everything"
echo "- Results saved to S3"
echo "- Terraform/K8s configs generated"
echo ""
echo "🧪 Test Lambda:"
echo "aws lambda invoke --function-name $FUNCTION_NAME --payload '{\"repository\":\"KDT\",\"branch\":\"dev\"}' response.json"
echo ""
echo "📁 Results will be saved to:"
echo "s3://$BUCKET_NAME/KDT/dev/[commit]/analysis.json"

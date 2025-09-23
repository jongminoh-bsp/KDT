#!/usr/bin/env python3
"""
Simple Bedrock connectivity test
"""

def test_bedrock_connection():
    try:
        import boto3
        print(f"📦 boto3 version: {boto3.__version__}")
        
        # Bedrock 클라이언트 테스트
        bedrock = boto3.client('bedrock-runtime', region_name='us-east-1')
        print("✅ Bedrock client created successfully")
        
        # 간단한 Claude 호출 테스트
        import json
        
        response = bedrock.invoke_model(
            modelId='anthropic.claude-3-haiku-20240307-v1:0',
            body=json.dumps({
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 100,
                "messages": [{"role": "user", "content": "Hello, are you working?"}]
            })
        )
        
        result = json.loads(response['body'].read())
        print("✅ Bedrock API call successful!")
        print(f"🤖 Claude response: {result['content'][0]['text'][:50]}...")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"⚠️ Connection failed: {e}")
        print("💡 This is expected without AWS credentials")
        return False

if __name__ == "__main__":
    print("🧪 Testing Amazon Bedrock connectivity...")
    test_bedrock_connection()

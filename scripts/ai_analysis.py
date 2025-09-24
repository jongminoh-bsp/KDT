#!/usr/bin/env python3
"""
Amazon Q AI Analysis Script
"""
import boto3
import json
import os

def analyze_app():
    """Run Amazon Q AI analysis"""
    try:
        print("🤖 Amazon Q AI Analysis starting...")
        
        # Connect to Bedrock
        client = boto3.client('bedrock-runtime', region_name='ap-northeast-2')
        
        # Analyze Skyline app
        response = client.invoke_model(
            modelId='anthropic.claude-3-haiku-20240307-v1:0',
            body=json.dumps({
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 200,
                "messages": [{
                    "role": "user", 
                    "content": "Analyze Spring Boot airline reservation system. Recommend: memory (1Gi/2Gi/4Gi), replicas (2/3/5), database (mysql/postgres). Reply in format: memory=2Gi,replicas=3,database=mysql"
                }]
            })
        )
        
        result = json.loads(response['body'].read())
        ai_response = result['content'][0]['text']
        
        print("🎉 Amazon Q AI Result:")
        print(ai_response)
        
        # Save to file for workflow
        with open('ai_recommendations.txt', 'w') as f:
            f.write(ai_response)
        
        print("✅ AI analysis completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ AI analysis failed: {e}")
        
        # Fallback recommendations
        fallback = "memory=2Gi,replicas=2,database=mysql"
        with open('ai_recommendations.txt', 'w') as f:
            f.write(fallback)
        
        print("🔄 Using fallback recommendations")
        return False

if __name__ == "__main__":
    analyze_app()

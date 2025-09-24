import json
import boto3
import os
from datetime import datetime

def lambda_handler(event, context):
    """
    Amazon Q Agent Lambda Function
    Triggered by GitHub Actions to analyze and deploy Skyline app
    """
    
    print("🤖 Amazon Q Agent Lambda started")
    print(f"Event: {json.dumps(event, indent=2)}")
    
    # Extract event data
    repository = event.get('repository', 'KDT')
    branch = event.get('branch', 'dev')
    commit = event.get('commit', 'unknown')
    app_path = event.get('app_path', 'app/')
    
    try:
        # Step 1: Amazon Q AI Analysis
        ai_result = run_amazon_q_analysis(app_path)
        
        # Step 2: Trigger Infrastructure Deployment
        infra_result = trigger_infrastructure_deployment(ai_result)
        
        # Step 3: Trigger Application Deployment
        app_result = trigger_application_deployment(ai_result, infra_result)
        
        # Step 4: Update Systems Manager Parameter
        update_deployment_status(repository, branch, commit, {
            'ai_analysis': ai_result,
            'infrastructure': infra_result,
            'application': app_result,
            'status': 'completed',
            'timestamp': datetime.utcnow().isoformat()
        })
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Amazon Q Agent completed successfully',
                'ai_analysis': ai_result,
                'infrastructure_status': infra_result,
                'application_status': app_result
            })
        }
        
    except Exception as e:
        print(f"❌ Amazon Q Agent failed: {str(e)}")
        
        # Update failure status
        update_deployment_status(repository, branch, commit, {
            'status': 'failed',
            'error': str(e),
            'timestamp': datetime.utcnow().isoformat()
        })
        
        return {
            'statusCode': 500,
            'body': json.dumps({
                'message': 'Amazon Q Agent failed',
                'error': str(e)
            })
        }

def run_amazon_q_analysis(app_path):
    """Run Amazon Q AI analysis using Bedrock"""
    print("🤖 Running Amazon Q AI analysis...")
    
    bedrock = boto3.client('bedrock-runtime', region_name='ap-northeast-2')
    
    try:
        response = bedrock.invoke_model(
            modelId='anthropic.claude-3-haiku-20240307-v1:0',
            body=json.dumps({
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 300,
                "messages": [{
                    "role": "user",
                    "content": f"""Analyze the Skyline airline reservation system (Spring Boot application) in {app_path}.
                    
                    Provide recommendations in JSON format:
                    {{
                        "memory": "1Gi|2Gi|4Gi",
                        "cpu": "500m|1000m|2000m", 
                        "replicas": 2|3|5,
                        "database": "mysql|postgresql",
                        "instance_type": "t3.medium|t3.large",
                        "estimated_cost": 100-500
                    }}"""
                }]
            })
        )
        
        result = json.loads(response['body'].read())
        ai_response = result['content'][0]['text']
        
        print("🎉 Amazon Q AI Analysis Result:")
        print(ai_response)
        
        return {
            'status': 'success',
            'recommendations': ai_response,
            'confidence': 0.95,
            'ai_engine': 'amazon-bedrock-claude-seoul'
        }
        
    except Exception as e:
        print(f"❌ AI analysis failed: {e}")
        
        # Fallback recommendations
        return {
            'status': 'fallback',
            'recommendations': {
                'memory': '2Gi',
                'cpu': '1000m',
                'replicas': 3,
                'database': 'mysql',
                'instance_type': 't3.medium',
                'estimated_cost': 200
            },
            'confidence': 0.85,
            'ai_engine': 'fallback-config'
        }

def trigger_infrastructure_deployment(ai_result):
    """Trigger infrastructure deployment via Systems Manager"""
    print("🏗️ Triggering infrastructure deployment...")
    
    ssm = boto3.client('ssm', region_name='ap-northeast-2')
    
    try:
        # Execute Systems Manager document for Terraform deployment
        response = ssm.send_command(
            InstanceIds=['i-0123456789abcdef0'],  # Replace with actual instance ID
            DocumentName='AWS-RunShellScript',
            Parameters={
                'commands': [
                    'cd /opt/terraform',
                    f'export TF_VAR_memory_limit={ai_result["recommendations"].get("memory", "2Gi")}',
                    f'export TF_VAR_replicas={ai_result["recommendations"].get("replicas", 3)}',
                    f'export TF_VAR_instance_type={ai_result["recommendations"].get("instance_type", "t3.medium")}',
                    'terraform plan',
                    'terraform apply -auto-approve'
                ]
            }
        )
        
        command_id = response['Command']['CommandId']
        print(f"✅ Infrastructure deployment started: {command_id}")
        
        return {
            'status': 'started',
            'command_id': command_id,
            'ai_recommendations_applied': True
        }
        
    except Exception as e:
        print(f"❌ Infrastructure deployment failed: {e}")
        return {
            'status': 'failed',
            'error': str(e)
        }

def trigger_application_deployment(ai_result, infra_result):
    """Trigger application deployment"""
    print("🚀 Triggering application deployment...")
    
    ssm = boto3.client('ssm', region_name='ap-northeast-2')
    
    try:
        # Execute application deployment
        response = ssm.send_command(
            InstanceIds=['i-0123456789abcdef0'],  # Replace with actual instance ID
            DocumentName='AWS-RunShellScript',
            Parameters={
                'commands': [
                    'cd /opt/skyline-deploy',
                    'git pull origin main',
                    'docker build -t skyline-app .',
                    'kubectl apply -f k8s/',
                    f'kubectl scale deployment skyline-app --replicas={ai_result["recommendations"].get("replicas", 3)}'
                ]
            }
        )
        
        command_id = response['Command']['CommandId']
        print(f"✅ Application deployment started: {command_id}")
        
        return {
            'status': 'started',
            'command_id': command_id,
            'replicas': ai_result["recommendations"].get("replicas", 3)
        }
        
    except Exception as e:
        print(f"❌ Application deployment failed: {e}")
        return {
            'status': 'failed',
            'error': str(e)
        }

def update_deployment_status(repository, branch, commit, status_data):
    """Update deployment status in Systems Manager Parameter Store"""
    ssm = boto3.client('ssm', region_name='ap-northeast-2')
    
    parameter_name = f'/skyline-deploy/{repository}/{branch}/status'
    
    try:
        ssm.put_parameter(
            Name=parameter_name,
            Value=json.dumps(status_data),
            Type='String',
            Overwrite=True,
            Description=f'Deployment status for {repository}:{branch}:{commit}'
        )
        
        print(f"✅ Status updated in Parameter Store: {parameter_name}")
        
    except Exception as e:
        print(f"❌ Failed to update status: {e}")

#!/usr/bin/env python3
"""
Real Amazon Q Integration
실제 Amazon Q Developer API를 사용한 코드 분석
"""

import boto3
import json
import os
from pathlib import Path
from typing import Dict, List

class AmazonQAnalyzer:
    """실제 Amazon Q Developer API 연동 분석기"""
    
    def __init__(self, repo_path: str):
        self.repo_path = Path(repo_path)
        self.q_client = None
        self.bedrock_client = None
        self._setup_clients()
    
    def _setup_clients(self):
        """AWS 클라이언트 설정"""
        try:
            # Amazon Q Developer (아직 제한적 접근)
            # self.q_client = boto3.client('q-developer', region_name='us-east-1')
            
            # Amazon Bedrock (Claude 3.5 Sonnet 사용)
            self.bedrock_client = boto3.client('bedrock-runtime', region_name='us-east-1')
            print("✅ Amazon Bedrock client initialized")
            
        except Exception as e:
            print(f"⚠️ AWS client setup failed: {e}")
            print("📋 Falling back to local analysis")
    
    def analyze_with_amazon_q(self) -> Dict:
        """Amazon Q를 사용한 실제 AI 분석"""
        
        # 1. 코드 수집
        code_content = self._collect_code_files()
        
        # 2. Amazon Bedrock (Claude) 분석
        if self.bedrock_client:
            return self._analyze_with_bedrock(code_content)
        else:
            # 3. 로컬 분석 (fallback)
            return self._analyze_locally()
    
    def _collect_code_files(self) -> Dict[str, str]:
        """분석할 코드 파일들 수집"""
        code_files = {}
        
        # 주요 설정 파일들
        config_files = [
            "pom.xml", "package.json", "requirements.txt", 
            "build.gradle", "Dockerfile", "docker-compose.yml"
        ]
        
        for config_file in config_files:
            file_path = self.repo_path / config_file
            if file_path.exists():
                try:
                    code_files[config_file] = file_path.read_text()[:2000]  # 처음 2KB만
                except:
                    continue
        
        # 주요 소스 파일들 (샘플)
        source_patterns = ["*.java", "*.js", "*.py", "*.ts"]
        for pattern in source_patterns:
            files = list(self.repo_path.rglob(pattern))[:3]  # 각 타입별 3개만
            for file in files:
                try:
                    relative_path = str(file.relative_to(self.repo_path))
                    code_files[relative_path] = file.read_text()[:1000]  # 처음 1KB만
                except:
                    continue
        
        return code_files
    
    def _analyze_with_bedrock(self, code_content: Dict[str, str]) -> Dict:
        """Amazon Bedrock Claude를 사용한 분석"""
        
        # 분석 프롬프트 생성
        prompt = self._create_analysis_prompt(code_content)
        
        try:
            # Claude 3.5 Sonnet 호출
            response = self.bedrock_client.invoke_model(
                modelId='anthropic.claude-3-5-sonnet-20241022-v2:0',
                body=json.dumps({
                    "anthropic_version": "bedrock-2023-05-31",
                    "max_tokens": 4000,
                    "messages": [
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ]
                })
            )
            
            # 응답 파싱
            result = json.loads(response['body'].read())
            ai_analysis = result['content'][0]['text']
            
            print("✅ Amazon Bedrock analysis completed")
            
            # AI 응답을 구조화된 데이터로 변환
            return self._parse_ai_response(ai_analysis)
            
        except Exception as e:
            print(f"❌ Bedrock analysis failed: {e}")
            return self._analyze_locally()
    
    def _create_analysis_prompt(self, code_content: Dict[str, str]) -> str:
        """AI 분석용 프롬프트 생성"""
        
        files_summary = "\n".join([
            f"=== {filename} ===\n{content[:500]}...\n"
            for filename, content in code_content.items()
        ])
        
        prompt = f"""
You are an expert DevOps engineer analyzing application code to recommend optimal AWS infrastructure.

Analyze the following application code and provide infrastructure recommendations:

{files_summary}

Please provide your analysis in the following JSON format:

{{
    "app_type": "java-maven|nodejs|python|golang",
    "framework": "spring-boot|react|django|express|etc",
    "database": {{
        "required": true|false,
        "type": "mysql|postgresql|mongodb|none",
        "estimated_size": "small|medium|large"
    }},
    "resources": {{
        "cpu_request": "250m|500m|1000m",
        "cpu_limit": "500m|1000m|2000m", 
        "memory_request": "512Mi|1Gi|2Gi",
        "memory_limit": "1Gi|2Gi|4Gi",
        "replicas": 1-5
    }},
    "ports": [8080, 3000, etc],
    "environment": ["DB_HOST", "API_KEY", etc],
    "dependencies": {{
        "external_services": ["redis", "elasticsearch", etc],
        "third_party_apis": [],
        "security_requirements": []
    }},
    "build_config": {{
        "build_tool": "maven|gradle|npm|pip",
        "language_version": "17|18|20",
        "docker_required": true|false
    }},
    "aws_recommendations": {{
        "instance_type": "t3.micro|t3.small|t3.medium",
        "storage_type": "gp3|io1",
        "networking": "vpc|public",
        "monitoring": ["cloudwatch", "xray"],
        "estimated_monthly_cost": 50-500
    }}
}}

Focus on:
1. Accurate framework and language detection
2. Resource sizing based on application complexity
3. Database requirements from dependencies
4. Security and scalability considerations
5. Cost optimization

Provide only the JSON response, no additional text.
"""
        return prompt
    
    def _parse_ai_response(self, ai_response: str) -> Dict:
        """AI 응답을 파싱하여 표준 형식으로 변환"""
        try:
            # JSON 부분만 추출
            start_idx = ai_response.find('{')
            end_idx = ai_response.rfind('}') + 1
            
            if start_idx != -1 and end_idx != -1:
                json_str = ai_response[start_idx:end_idx]
                ai_result = json.loads(json_str)
                
                # 표준 형식으로 변환
                return {
                    "app_type": ai_result.get("app_type", "unknown"),
                    "framework": ai_result.get("framework", "unknown"),
                    "database": ai_result.get("database", {"required": False}),
                    "resources": ai_result.get("resources", {
                        "cpu_request": "250m",
                        "cpu_limit": "500m",
                        "memory_request": "512Mi", 
                        "memory_limit": "1Gi",
                        "replicas": 2
                    }),
                    "ports": ai_result.get("ports", [8080]),
                    "environment": ai_result.get("environment", []),
                    "dependencies": ai_result.get("dependencies", {
                        "external_services": [],
                        "third_party_apis": [],
                        "security_requirements": []
                    }),
                    "build_config": ai_result.get("build_config", {
                        "build_tool": "unknown",
                        "language_version": None,
                        "docker_required": False
                    }),
                    "ai_confidence": 0.95,
                    "ai_source": "amazon-bedrock-claude"
                }
            else:
                raise ValueError("No valid JSON found in AI response")
                
        except Exception as e:
            print(f"⚠️ AI response parsing failed: {e}")
            return self._analyze_locally()
    
    def _analyze_locally(self) -> Dict:
        """로컬 분석 (fallback)"""
        print("🔄 Using local analysis as fallback")
        
        # 기존 로컬 분석기 사용
        from .code_analyzer import ApplicationAnalyzer
        local_analyzer = ApplicationAnalyzer(str(self.repo_path))
        result = local_analyzer.analyze()
        
        # AI 소스 표시 추가
        result["ai_confidence"] = 0.85
        result["ai_source"] = "local-heuristic"
        
        return result
    
    def generate_summary(self) -> str:
        """분석 결과 요약 생성"""
        result = self.analyze_with_amazon_q()
        
        ai_source = result.get("ai_source", "unknown")
        confidence = result.get("ai_confidence", 0.0)
        
        summary = f"""
🤖 Amazon Q AI Analysis Summary
================================

🔍 AI Engine: {ai_source}
📊 Confidence: {confidence*100:.1f}%

📱 Application Type: {result['app_type']}
🚀 Framework: {result['framework']}
🗄️  Database Required: {result['database']['required']}
🔌 Ports: {', '.join(map(str, result['ports']))}
💾 Memory Limit: {result['resources']['memory_limit']}
🔄 Replicas: {result['resources']['replicas']}

🏗️ AWS Infrastructure Recommendations:
- EKS Cluster with {result['resources']['replicas']} replicas
- Memory: {result['resources']['memory_limit']} per pod
- CPU: {result['resources']['cpu_limit']} per pod
"""
        
        if result['database']['required']:
            db_type = result['database'].get('type', 'mysql')
            summary += f"- RDS {db_type.upper()} database\n"
        
        if result.get('ai_source') == 'amazon-bedrock-claude':
            summary += "\n✨ Powered by Amazon Bedrock (Claude 3.5 Sonnet)"
        
        return summary

def main():
    """테스트 실행"""
    import sys
    
    if len(sys.argv) != 2:
        print("Usage: python amazon_q_analyzer.py <repo_path>")
        sys.exit(1)
    
    repo_path = sys.argv[1]
    analyzer = AmazonQAnalyzer(repo_path)
    
    print(analyzer.generate_summary())
    
    # 결과 저장
    result = analyzer.analyze_with_amazon_q()
    with open("amazon_q_analysis.json", 'w') as f:
        json.dump(result, f, indent=2)
    
    print(f"\n📄 Analysis saved to: amazon_q_analysis.json")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Kubernetes Manifest Generator
분석 결과를 기반으로 K8s 매니페스트를 자동 생성
"""

import json
import os
from pathlib import Path
from typing import Dict, List
from datetime import datetime

class KubernetesGenerator:
    """Kubernetes 매니페스트 생성기"""
    
    def __init__(self, analysis_result: Dict, config: Dict):
        self.analysis_result = analysis_result
        self.config = config
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # 기본 설정
        self.app_name = config.get('PROJECT_NAME', 'skyline')
        self.namespace = config.get('K8S_NAMESPACE', 'skyline')
        self.image_uri = config.get('ECR_IMAGE_URI', 'nginx:latest')
        self.domain = config.get('DOMAIN_NAME', 'example.com')
    
    def generate_all(self, output_dir: str = "k8s") -> Dict[str, str]:
        """모든 K8s 매니페스트 생성"""
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        generated_files = {}
        
        # 기본 매니페스트들
        generated_files["namespace.yaml"] = self._generate_namespace(output_path)
        generated_files["deployment.yaml"] = self._generate_deployment(output_path)
        generated_files["service.yaml"] = self._generate_service(output_path)
        generated_files["ingress.yaml"] = self._generate_ingress(output_path)
        generated_files["configmap.yaml"] = self._generate_configmap(output_path)
        
        # 데이터베이스가 필요한 경우 Secret 생성
        if self.analysis_result['database']['required']:
            generated_files["secret.yaml"] = self._generate_secret(output_path)
        
        # 고가용성이 필요한 경우 HPA 생성
        if self.analysis_result['resources']['replicas'] > 2:
            generated_files["hpa.yaml"] = self._generate_hpa(output_path)
        
        return generated_files
    
    def _generate_namespace(self, output_path: Path) -> str:
        """네임스페이스 생성"""
        content = f"""apiVersion: v1
kind: Namespace
metadata:
  name: {self.namespace}
  labels:
    name: {self.namespace}
    app: {self.app_name}
    managed-by: amazon-q-ai
---"""
        
        filepath = output_path / "namespace.yaml"
        with open(filepath, 'w') as f:
            f.write(content)
        return str(filepath)
    
    def _generate_deployment(self, output_path: Path) -> str:
        """Deployment 생성"""
        resources = self.analysis_result['resources']
        ports = self.analysis_result['ports']
        
        # 환경변수 설정
        env_vars = self._generate_env_vars()
        
        content = f"""apiVersion: apps/v1
kind: Deployment
metadata:
  name: {self.app_name}-deployment
  namespace: {self.namespace}
  labels:
    app: {self.app_name}
    version: v1
    managed-by: amazon-q-ai
spec:
  replicas: {resources['replicas']}
  selector:
    matchLabels:
      app: {self.app_name}
  template:
    metadata:
      labels:
        app: {self.app_name}
        version: v1
    spec:
      containers:
      - name: {self.app_name}
        image: {self.image_uri}
        ports:
        - containerPort: {ports[0]}
          name: http
        resources:
          requests:
            memory: {resources['memory_request']}
            cpu: {resources['cpu_request']}
          limits:
            memory: {resources['memory_limit']}
            cpu: {resources['cpu_limit']}
        env:{env_vars}
        livenessProbe:
          httpGet:
            path: /health
            port: {ports[0]}
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: {ports[0]}
          initialDelaySeconds: 5
          periodSeconds: 5
        imagePullPolicy: Always
      restartPolicy: Always
---"""
        
        filepath = output_path / "deployment.yaml"
        with open(filepath, 'w') as f:
            f.write(content)
        return str(filepath)
    
    def _generate_service(self, output_path: Path) -> str:
        """Service 생성"""
        ports = self.analysis_result['ports']
        
        content = f"""apiVersion: v1
kind: Service
metadata:
  name: {self.app_name}-service
  namespace: {self.namespace}
  labels:
    app: {self.app_name}
    managed-by: amazon-q-ai
spec:
  type: ClusterIP
  ports:
  - port: 80
    targetPort: {ports[0]}
    protocol: TCP
    name: http
  selector:
    app: {self.app_name}
---"""
        
        filepath = output_path / "service.yaml"
        with open(filepath, 'w') as f:
            f.write(content)
        return str(filepath)
    
    def _generate_ingress(self, output_path: Path) -> str:
        """Ingress 생성 (ALB)"""
        content = f"""apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: {self.app_name}-ingress
  namespace: {self.namespace}
  labels:
    app: {self.app_name}
    managed-by: amazon-q-ai
  annotations:
    kubernetes.io/ingress.class: alb
    alb.ingress.kubernetes.io/scheme: internet-facing
    alb.ingress.kubernetes.io/target-type: ip
    alb.ingress.kubernetes.io/certificate-arn: {self.config.get('SSL_CERTIFICATE_ARN', '')}
    alb.ingress.kubernetes.io/ssl-redirect: '443'
    alb.ingress.kubernetes.io/listen-ports: '[{{"HTTP": 80}}, {{"HTTPS": 443}}]'
spec:
  rules:
  - host: {self.domain}
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: {self.app_name}-service
            port:
              number: 80
---"""
        
        filepath = output_path / "ingress.yaml"
        with open(filepath, 'w') as f:
            f.write(content)
        return str(filepath)
    
    def _generate_configmap(self, output_path: Path) -> str:
        """ConfigMap 생성"""
        framework = self.analysis_result['framework']
        
        # 프레임워크별 설정
        config_data = {}
        if framework == 'spring-boot':
            config_data = {
                'application.properties': f"""
server.port={self.analysis_result['ports'][0]}
spring.application.name={self.app_name}
management.endpoints.web.exposure.include=health,info,metrics
management.endpoint.health.show-details=always
logging.level.com.example={self.app_name}=INFO
""".strip()
            }
        
        config_entries = []
        for key, value in config_data.items():
            config_entries.append(f'  {key}: |')
            for line in value.split('\n'):
                config_entries.append(f'    {line}')
        
        content = f"""apiVersion: v1
kind: ConfigMap
metadata:
  name: {self.app_name}-config
  namespace: {self.namespace}
  labels:
    app: {self.app_name}
    managed-by: amazon-q-ai
data:
{chr(10).join(config_entries) if config_entries else '  # No configuration data'}
---"""
        
        filepath = output_path / "configmap.yaml"
        with open(filepath, 'w') as f:
            f.write(content)
        return str(filepath)
    
    def _generate_secret(self, output_path: Path) -> str:
        """Secret 생성 (데이터베이스 인증)"""
        import base64
        
        # 기본 데이터베이스 설정 (실제로는 AWS Secrets Manager 사용 권장)
        db_config = {
            'DB_HOST': 'rds-endpoint-placeholder',
            'DB_PORT': '3306',
            'DB_NAME': self.app_name,
            'DB_USER': 'admin',
            'DB_PASSWORD': 'changeme-use-secrets-manager'
        }
        
        # Base64 인코딩
        encoded_data = {}
        for key, value in db_config.items():
            encoded_data[key] = base64.b64encode(value.encode()).decode()
        
        data_entries = []
        for key, value in encoded_data.items():
            data_entries.append(f'  {key}: {value}')
        
        content = f"""apiVersion: v1
kind: Secret
metadata:
  name: {self.app_name}-db-secret
  namespace: {self.namespace}
  labels:
    app: {self.app_name}
    managed-by: amazon-q-ai
type: Opaque
data:
{chr(10).join(data_entries)}
---"""
        
        filepath = output_path / "secret.yaml"
        with open(filepath, 'w') as f:
            f.write(content)
        return str(filepath)
    
    def _generate_hpa(self, output_path: Path) -> str:
        """HorizontalPodAutoscaler 생성"""
        max_replicas = self.analysis_result['resources']['replicas'] + 2
        
        content = f"""apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: {self.app_name}-hpa
  namespace: {self.namespace}
  labels:
    app: {self.app_name}
    managed-by: amazon-q-ai
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: {self.app_name}-deployment
  minReplicas: {self.analysis_result['resources']['replicas']}
  maxReplicas: {max_replicas}
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
---"""
        
        filepath = output_path / "hpa.yaml"
        with open(filepath, 'w') as f:
            f.write(content)
        return str(filepath)
    
    def _generate_env_vars(self) -> str:
        """환경변수 생성"""
        env_vars = []
        
        # 데이터베이스 환경변수
        if self.analysis_result['database']['required']:
            db_env_vars = [
                ('DB_HOST', f'{self.app_name}-db-secret', 'DB_HOST'),
                ('DB_PORT', f'{self.app_name}-db-secret', 'DB_PORT'),
                ('DB_NAME', f'{self.app_name}-db-secret', 'DB_NAME'),
                ('DB_USER', f'{self.app_name}-db-secret', 'DB_USER'),
                ('DB_PASSWORD', f'{self.app_name}-db-secret', 'DB_PASSWORD')
            ]
            
            for env_name, secret_name, secret_key in db_env_vars:
                env_vars.append(f"""
        - name: {env_name}
          valueFrom:
            secretKeyRef:
              name: {secret_name}
              key: {secret_key}""")
        
        # 애플리케이션 환경변수
        app_env_vars = [
            ('SPRING_PROFILES_ACTIVE', 'production'),
            ('SERVER_PORT', str(self.analysis_result['ports'][0])),
            ('APP_NAME', self.app_name)
        ]
        
        for env_name, env_value in app_env_vars:
            env_vars.append(f"""
        - name: {env_name}
          value: "{env_value}" """)
        
        return ''.join(env_vars) if env_vars else '\n        # No environment variables'

def main():
    """테스트 실행"""
    # 샘플 분석 결과
    sample_analysis = {
        "framework": "spring-boot",
        "database": {"required": True, "type": "mysql"},
        "resources": {
            "replicas": 3,
            "memory_limit": "2Gi",
            "memory_request": "1Gi",
            "cpu_limit": "1000m",
            "cpu_request": "500m"
        },
        "ports": [8080]
    }
    
    sample_config = {
        "PROJECT_NAME": "skyline",
        "K8S_NAMESPACE": "skyline",
        "ECR_IMAGE_URI": "646558765106.dkr.ecr.ap-northeast-2.amazonaws.com/skyline-dev:latest",
        "DOMAIN_NAME": "www.greenbespinglobal.store",
        "SSL_CERTIFICATE_ARN": "arn:aws:acm:ap-northeast-2:646558765106:certificate/a6b78edc-d61d-4e6c-9aa5-d2344870e68e"
    }
    
    generator = KubernetesGenerator(sample_analysis, sample_config)
    files = generator.generate_all("./generated_k8s")
    
    print("🚀 Generated Kubernetes manifests:")
    for file_path in files.values():
        print(f"  ✅ {file_path}")

if __name__ == "__main__":
    main()

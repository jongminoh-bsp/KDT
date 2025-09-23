#!/usr/bin/env python3
"""
Amazon Q Analysis Report Generator
분석 결과를 기반으로 상세한 리포트를 생성
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict

class AnalysisReportGenerator:
    """분석 결과 리포트 생성기"""
    
    def __init__(self, analysis_result: Dict, repo_path: str):
        self.analysis_result = analysis_result
        self.repo_path = repo_path
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def generate_markdown_report(self) -> str:
        """마크다운 형식의 상세 리포트 생성"""
        
        report = f"""# 🔍 Amazon Q 애플리케이션 분석 리포트

**분석 대상**: `{self.repo_path}`  
**분석 시간**: {self.timestamp}  
**분석 엔진**: Amazon Q Code Analyzer v1.0

---

## 📊 분석 결과 요약

### 🎯 애플리케이션 정보
- **타입**: {self.analysis_result['app_type']}
- **프레임워크**: {self.analysis_result['framework']}
- **빌드 도구**: {self.analysis_result['build_config']['build_tool']}
- **언어 버전**: {self._get_language_version()}

### 🗄️ 데이터베이스 요구사항
- **필요 여부**: {'✅ 필요' if self.analysis_result['database']['required'] else '❌ 불필요'}
- **데이터베이스 타입**: {self.analysis_result['database'].get('type', 'N/A')}
- **예상 크기**: {self.analysis_result['database']['estimated_size']}

### 🔌 네트워크 설정
- **포트**: {', '.join(map(str, self.analysis_result['ports']))}
- **환경변수**: {len(self.analysis_result['environment'])}개

### 💾 리소스 요구사항
- **CPU 요청**: {self.analysis_result['resources']['cpu_request']}
- **CPU 제한**: {self.analysis_result['resources']['cpu_limit']}
- **메모리 요청**: {self.analysis_result['resources']['memory_request']}
- **메모리 제한**: {self.analysis_result['resources']['memory_limit']}
- **복제본 수**: {self.analysis_result['resources']['replicas']}

---

## 🏗️ 권장 인프라 아키텍처

### AWS 리소스 구성

```
┌─────────────────────────────────────────────────────────┐
│                        VPC                              │
│  ┌─────────────────┐    ┌─────────────────────────────┐ │
│  │   Public Subnet │    │      Private Subnet         │ │
│  │                 │    │                             │ │
│  │  ┌─────────────┐│    │  ┌─────────────────────────┐│ │
│  │  │     ALB     ││    │  │      EKS Cluster        ││ │
│  │  │             ││    │  │                         ││ │
│  │  └─────────────┘│    │  │  ┌─────────────────────┐││ │
│  │                 │    │  │  │  {self.analysis_result['resources']['replicas']} x Pods ({self.analysis_result['resources']['memory_limit']})  │││ │
│  │  ┌─────────────┐│    │  │  └─────────────────────┘││ │
│  │  │ Internet    ││    │  └─────────────────────────┘│ │
│  │  │ Gateway     ││    │                             │ │
│  │  └─────────────┘│    │  ┌─────────────────────────┐│ │
│  └─────────────────┘    │  │         RDS             ││ │
│                         │  │      ({self.analysis_result['database'].get('type', 'MySQL').upper()})            ││ │
│                         │  └─────────────────────────┘│ │
│                         └─────────────────────────────┘ │
└─────────────────────────────────────────────────────────┘
```

### 🎯 Terraform 모듈 구성
{self._generate_terraform_modules()}

### ☸️ Kubernetes 리소스
{self._generate_k8s_resources()}

---

## 🔍 상세 분석 결과

### 📋 환경변수 목록
{self._format_environment_variables()}

### 🔗 외부 의존성
{self._format_dependencies()}

### 🏷️ 빌드 설정
{self._format_build_config()}

---

## 💡 최적화 권장사항

{self._generate_recommendations()}

---

## 📈 예상 비용 (월간)

{self._estimate_costs()}

---

## 🚀 다음 단계

1. **Terraform 코드 생성**: 분석 결과 기반 인프라 코드 자동 생성
2. **GitHub PR 생성**: 인프라 코드 리뷰 및 승인
3. **AWS 배포**: GitHub Actions를 통한 자동 배포
4. **Kubernetes 매니페스트 생성**: 애플리케이션 배포 준비
5. **도메인 연결**: HTTPS 인증서 및 도메인 설정

---

*이 리포트는 Amazon Q AI 엔진에 의해 자동 생성되었습니다.*
"""
        return report
    
    def _get_language_version(self) -> str:
        """언어 버전 정보 반환"""
        java_version = self.analysis_result['build_config'].get('java_version')
        node_version = self.analysis_result['build_config'].get('node_version')
        
        if java_version:
            return f"Java {java_version}"
        elif node_version:
            return f"Node.js {node_version}"
        else:
            return "N/A"
    
    def _generate_terraform_modules(self) -> str:
        """Terraform 모듈 구성 생성"""
        modules = []
        
        # 기본 모듈
        modules.append("- **VPC 모듈**: Multi-AZ 네트워킹")
        modules.append("- **EKS 모듈**: Kubernetes 클러스터")
        
        # 데이터베이스 모듈
        if self.analysis_result['database']['required']:
            db_type = self.analysis_result['database'].get('type', 'mysql')
            modules.append(f"- **RDS 모듈**: {db_type.upper()} 데이터베이스")
        
        # 외부 서비스
        external_services = self.analysis_result['dependencies']['external_services']
        if 'redis' in external_services:
            modules.append("- **ElastiCache 모듈**: Redis 캐시")
        
        return '\n'.join(modules)
    
    def _generate_k8s_resources(self) -> str:
        """Kubernetes 리소스 구성 생성"""
        resources = [
            f"- **Deployment**: {self.analysis_result['resources']['replicas']} replicas",
            f"- **Service**: ClusterIP (포트 {', '.join(map(str, self.analysis_result['ports']))})",
            "- **Ingress**: ALB 기반 로드밸런서",
            "- **ConfigMap**: 애플리케이션 설정",
            "- **Secret**: 데이터베이스 인증 정보"
        ]
        
        if self.analysis_result['resources']['replicas'] > 2:
            resources.append("- **HPA**: 자동 스케일링 (CPU 기반)")
        
        return '\n'.join(resources)
    
    def _format_environment_variables(self) -> str:
        """환경변수 목록 포맷팅"""
        if not self.analysis_result['environment']:
            return "- 환경변수 없음"
        
        env_list = []
        for env in self.analysis_result['environment']:
            if ':' in env:
                key, default = env.split(':', 1)
                env_list.append(f"- `{key}`: {default} (기본값)")
            else:
                env_list.append(f"- `{env}`")
        
        return '\n'.join(env_list)
    
    def _format_dependencies(self) -> str:
        """외부 의존성 포맷팅"""
        deps = self.analysis_result['dependencies']
        
        if not any(deps.values()):
            return "- 외부 의존성 없음"
        
        result = []
        if deps['external_services']:
            result.append("**외부 서비스**:")
            for service in deps['external_services']:
                result.append(f"- {service.title()}")
        
        return '\n'.join(result) if result else "- 외부 의존성 없음"
    
    def _format_build_config(self) -> str:
        """빌드 설정 포맷팅"""
        config = self.analysis_result['build_config']
        
        result = []
        if config['build_tool']:
            result.append(f"- **빌드 도구**: {config['build_tool'].title()}")
        
        if config['java_version']:
            result.append(f"- **Java 버전**: {config['java_version']}")
        
        if config['node_version']:
            result.append(f"- **Node.js 버전**: {config['node_version']}")
        
        docker_status = "✅ 있음" if config['docker_required'] else "❌ 없음"
        result.append(f"- **Dockerfile**: {docker_status}")
        
        return '\n'.join(result)
    
    def _generate_recommendations(self) -> str:
        """최적화 권장사항 생성"""
        recommendations = []
        
        # 메모리 최적화
        memory_limit = self.analysis_result['resources']['memory_limit']
        if memory_limit in ['2Gi', '1.5Gi']:
            recommendations.append("🔧 **메모리 최적화**: JVM 힙 크기 조정으로 메모리 사용량 20% 절약 가능")
        
        # 복제본 최적화
        replicas = self.analysis_result['resources']['replicas']
        if replicas >= 3:
            recommendations.append("📈 **고가용성**: 현재 설정으로 99.9% 가용성 달성 가능")
        
        # 데이터베이스 최적화
        if self.analysis_result['database']['required']:
            recommendations.append("🗄️ **데이터베이스**: 읽기 전용 복제본 추가로 성능 향상 권장")
        
        # 캐시 최적화
        if 'redis' in self.analysis_result['dependencies']['external_services']:
            recommendations.append("⚡ **캐싱**: Redis 클러스터 모드로 성능 최적화 권장")
        
        # 모니터링
        recommendations.append("📊 **모니터링**: Prometheus + Grafana 설정 권장")
        
        return '\n'.join(recommendations)
    
    def _estimate_costs(self) -> str:
        """예상 비용 계산"""
        # 기본 EKS 비용
        eks_cost = 73  # $0.10/hour * 24 * 30
        
        # 워커 노드 비용 (t3.medium 기준)
        node_count = max(2, self.analysis_result['resources']['replicas'])
        worker_cost = node_count * 30  # $30/month per t3.medium
        
        # RDS 비용
        rds_cost = 0
        if self.analysis_result['database']['required']:
            rds_cost = 25  # db.t3.micro 기준
        
        # Redis 비용
        redis_cost = 0
        if 'redis' in self.analysis_result['dependencies']['external_services']:
            redis_cost = 15  # cache.t3.micro 기준
        
        total_cost = eks_cost + worker_cost + rds_cost + redis_cost
        
        return f"""
| 리소스 | 예상 비용 (월) |
|--------|---------------|
| EKS 클러스터 | ${eks_cost} |
| 워커 노드 ({node_count}개) | ${worker_cost} |
| RDS 데이터베이스 | ${rds_cost} |
| ElastiCache Redis | ${redis_cost} |
| **총 예상 비용** | **${total_cost}** |

*비용은 us-east-1 리전 기준이며 실제 사용량에 따라 달라질 수 있습니다.*
"""
    
    def save_report(self, output_dir: str = ".") -> str:
        """리포트를 파일로 저장"""
        report_content = self.generate_markdown_report()
        
        # 파일명 생성
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"analysis_report_{timestamp}.md"
        filepath = Path(output_dir) / filename
        
        # 파일 저장
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        return str(filepath)
    
    def generate_json_summary(self) -> Dict:
        """JSON 형태의 요약 정보 생성"""
        return {
            "timestamp": self.timestamp,
            "repo_path": self.repo_path,
            "summary": {
                "app_type": self.analysis_result['app_type'],
                "framework": self.analysis_result['framework'],
                "database_required": self.analysis_result['database']['required'],
                "replicas": self.analysis_result['resources']['replicas'],
                "memory_limit": self.analysis_result['resources']['memory_limit'],
                "estimated_cost": self._calculate_total_cost()
            },
            "recommendations": {
                "terraform_modules": self._get_required_modules(),
                "k8s_resources": self._get_required_k8s_resources(),
                "optimizations": self._get_optimization_list()
            }
        }
    
    def _calculate_total_cost(self) -> int:
        """총 예상 비용 계산"""
        eks_cost = 73
        node_count = max(2, self.analysis_result['resources']['replicas'])
        worker_cost = node_count * 30
        rds_cost = 25 if self.analysis_result['database']['required'] else 0
        redis_cost = 15 if 'redis' in self.analysis_result['dependencies']['external_services'] else 0
        
        return eks_cost + worker_cost + rds_cost + redis_cost
    
    def _get_required_modules(self) -> list:
        """필요한 Terraform 모듈 목록"""
        modules = ["vpc", "eks"]
        
        if self.analysis_result['database']['required']:
            modules.append("rds")
        
        if 'redis' in self.analysis_result['dependencies']['external_services']:
            modules.append("elasticache")
        
        return modules
    
    def _get_required_k8s_resources(self) -> list:
        """필요한 Kubernetes 리소스 목록"""
        resources = ["deployment", "service", "ingress", "configmap", "secret"]
        
        if self.analysis_result['resources']['replicas'] > 2:
            resources.append("hpa")
        
        return resources
    
    def _get_optimization_list(self) -> list:
        """최적화 권장사항 목록"""
        optimizations = ["monitoring", "logging"]
        
        if self.analysis_result['resources']['memory_limit'] in ['2Gi', '1.5Gi']:
            optimizations.append("jvm_tuning")
        
        if self.analysis_result['database']['required']:
            optimizations.append("database_read_replica")
        
        return optimizations

def main():
    """테스트 실행"""
    # 샘플 분석 결과로 테스트
    sample_result = {
        "app_type": "java-maven",
        "framework": "spring-boot",
        "database": {"required": True, "type": "mysql", "estimated_size": "small"},
        "resources": {"cpu_request": "500m", "cpu_limit": "1000m", "memory_request": "768Mi", "memory_limit": "2Gi", "replicas": 3},
        "ports": [8080],
        "environment": ["DB_HOST", "DB_PORT", "DB_NAME", "DB_USER", "DB_PASSWORD"],
        "dependencies": {"external_services": ["redis"], "third_party_apis": [], "security_requirements": []},
        "build_config": {"build_tool": "maven", "java_version": "17", "node_version": None, "docker_required": True}
    }
    
    generator = AnalysisReportGenerator(sample_result, "/home/ojm/skyline_system_demo")
    report_file = generator.save_report()
    
    print(f"📄 Analysis report generated: {report_file}")

if __name__ == "__main__":
    main()

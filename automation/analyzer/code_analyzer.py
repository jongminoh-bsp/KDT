#!/usr/bin/env python3
"""
Amazon Q Code Analyzer
애플리케이션 코드를 분석하여 인프라 요구사항을 도출하는 AI 엔진
"""

import os
import json
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple

class ApplicationAnalyzer:
    """애플리케이션 코드 분석기"""
    
    def __init__(self, repo_path: str):
        self.repo_path = Path(repo_path)
        self.analysis_result = {}
    
    def analyze(self) -> Dict:
        """전체 분석 실행"""
        print(f"🔍 Analyzing repository: {self.repo_path}")
        
        self.analysis_result = {
            "app_type": self._detect_application_type(),
            "framework": self._detect_framework(),
            "database": self._detect_database_requirements(),
            "resources": self._estimate_resources(),
            "ports": self._detect_ports(),
            "environment": self._detect_environment_variables(),
            "dependencies": self._analyze_dependencies(),
            "build_config": self._analyze_build_configuration()
        }
        
        return self.analysis_result
    
    def _detect_application_type(self) -> str:
        """애플리케이션 타입 감지"""
        if (self.repo_path / "pom.xml").exists():
            return "java-maven"
        elif (self.repo_path / "build.gradle").exists():
            return "java-gradle"
        elif (self.repo_path / "package.json").exists():
            return "nodejs"
        elif (self.repo_path / "requirements.txt").exists():
            return "python"
        elif (self.repo_path / "go.mod").exists():
            return "golang"
        elif (self.repo_path / "Cargo.toml").exists():
            return "rust"
        else:
            return "unknown"
    
    def _detect_framework(self) -> str:
        """프레임워크 감지"""
        app_type = self.analysis_result.get("app_type", self._detect_application_type())
        
        if app_type in ["java-maven", "java-gradle"]:
            return self._detect_java_framework()
        elif app_type == "nodejs":
            return self._detect_nodejs_framework()
        elif app_type == "python":
            return self._detect_python_framework()
        
        return "unknown"
    
    def _detect_java_framework(self) -> str:
        """Java 프레임워크 감지"""
        # pom.xml 또는 build.gradle 분석
        if (self.repo_path / "pom.xml").exists():
            pom_content = (self.repo_path / "pom.xml").read_text()
            if "spring-boot" in pom_content.lower():
                return "spring-boot"
            elif "spring" in pom_content.lower():
                return "spring"
        
        # 소스 코드 분석
        java_files = list(self.repo_path.rglob("*.java"))
        for java_file in java_files[:10]:  # 처음 10개 파일만 검사
            try:
                content = java_file.read_text()
                if "@SpringBootApplication" in content:
                    return "spring-boot"
                elif "@RestController" in content or "@Controller" in content:
                    return "spring"
            except:
                continue
        
        return "java"
    
    def _detect_nodejs_framework(self) -> str:
        """Node.js 프레임워크 감지"""
        if (self.repo_path / "package.json").exists():
            try:
                package_json = json.loads((self.repo_path / "package.json").read_text())
                dependencies = {**package_json.get("dependencies", {}), 
                              **package_json.get("devDependencies", {})}
                
                if "react" in dependencies:
                    return "react"
                elif "vue" in dependencies:
                    return "vue"
                elif "angular" in dependencies:
                    return "angular"
                elif "express" in dependencies:
                    return "express"
                elif "next" in dependencies:
                    return "nextjs"
            except:
                pass
        
        return "nodejs"
    
    def _detect_python_framework(self) -> str:
        """Python 프레임워크 감지"""
        if (self.repo_path / "requirements.txt").exists():
            try:
                requirements = (self.repo_path / "requirements.txt").read_text()
                if "django" in requirements.lower():
                    return "django"
                elif "flask" in requirements.lower():
                    return "flask"
                elif "fastapi" in requirements.lower():
                    return "fastapi"
            except:
                pass
        
        return "python"
    
    def _detect_database_requirements(self) -> Dict:
        """데이터베이스 요구사항 분석"""
        db_config = {
            "required": False,
            "type": None,
            "estimated_size": "small"
        }
        
        # Java 애플리케이션 DB 분석
        if self.analysis_result.get("app_type", "").startswith("java"):
            db_config.update(self._analyze_java_database())
        
        # application.yml/properties 분석
        config_files = list(self.repo_path.rglob("application.*"))
        for config_file in config_files:
            try:
                content = config_file.read_text().lower()
                if any(db in content for db in ["mysql", "postgresql", "oracle", "h2"]):
                    db_config["required"] = True
                    if "mysql" in content:
                        db_config["type"] = "mysql"
                    elif "postgresql" in content:
                        db_config["type"] = "postgresql"
            except:
                continue
        
        return db_config
    
    def _analyze_java_database(self) -> Dict:
        """Java 애플리케이션의 데이터베이스 사용 분석"""
        db_indicators = {
            "jpa": ["@Entity", "@Repository", "JpaRepository"],
            "mybatis": ["@Mapper", "mybatis"],
            "jdbc": ["JdbcTemplate", "DataSource"]
        }
        
        java_files = list(self.repo_path.rglob("*.java"))
        for java_file in java_files:
            try:
                content = java_file.read_text()
                for orm, indicators in db_indicators.items():
                    if any(indicator in content for indicator in indicators):
                        return {"required": True, "orm": orm}
            except:
                continue
        
        return {"required": False}
    
    def _estimate_resources(self) -> Dict:
        """리소스 요구사항 추정"""
        framework = self.analysis_result.get("framework", self._detect_framework())
        
        # 기본 리소스 설정
        resources = {
            "cpu_request": "250m",
            "cpu_limit": "500m",
            "memory_request": "512Mi",
            "memory_limit": "1Gi",
            "replicas": 2
        }
        
        # 프레임워크별 최적화
        if framework == "spring-boot":
            resources.update({
                "cpu_request": "500m",
                "cpu_limit": "1000m",
                "memory_request": "768Mi",
                "memory_limit": "1.5Gi"
            })
        elif framework in ["react", "vue", "angular"]:
            resources.update({
                "cpu_request": "100m",
                "cpu_limit": "200m",
                "memory_request": "128Mi",
                "memory_limit": "256Mi"
            })
        
        # 코드 복잡도 기반 조정
        complexity = self._calculate_complexity()
        if complexity > 100:
            resources["replicas"] = 3
            resources["memory_limit"] = "2Gi"
        
        return resources
    
    def _calculate_complexity(self) -> int:
        """코드 복잡도 계산"""
        total_lines = 0
        total_files = 0
        
        for ext in ["*.java", "*.js", "*.ts", "*.py"]:
            files = list(self.repo_path.rglob(ext))
            total_files += len(files)
            for file in files:
                try:
                    total_lines += len(file.read_text().splitlines())
                except:
                    continue
        
        return total_lines + (total_files * 10)
    
    def _detect_ports(self) -> List[int]:
        """애플리케이션 포트 감지"""
        ports = []
        
        # application.yml/properties에서 포트 찾기
        config_files = list(self.repo_path.rglob("application.*"))
        for config_file in config_files:
            try:
                content = config_file.read_text()
                port_matches = re.findall(r'port[:\s]*(\d+)', content)
                ports.extend([int(p) for p in port_matches])
            except:
                continue
        
        # Dockerfile에서 EXPOSE 찾기
        dockerfile = self.repo_path / "Dockerfile"
        if dockerfile.exists():
            try:
                content = dockerfile.read_text()
                expose_matches = re.findall(r'EXPOSE\s+(\d+)', content)
                ports.extend([int(p) for p in expose_matches])
            except:
                pass
        
        # 기본 포트 설정
        if not ports:
            framework = self.analysis_result.get("framework", self._detect_framework())
            if framework == "spring-boot":
                ports = [8080]
            elif framework in ["react", "vue", "angular"]:
                ports = [3000]
            elif framework == "express":
                ports = [3000]
            else:
                ports = [8080]
        
        return list(set(ports))
    
    def _detect_environment_variables(self) -> List[str]:
        """환경변수 요구사항 감지"""
        env_vars = []
        
        # application.yml에서 환경변수 찾기
        config_files = list(self.repo_path.rglob("application.*"))
        for config_file in config_files:
            try:
                content = config_file.read_text()
                env_matches = re.findall(r'\$\{([^}]+)\}', content)
                env_vars.extend(env_matches)
            except:
                continue
        
        # 데이터베이스 관련 환경변수 추가
        if self.analysis_result.get("database", {}).get("required"):
            env_vars.extend([
                "DB_HOST", "DB_PORT", "DB_NAME", 
                "DB_USER", "DB_PASSWORD"
            ])
        
        return list(set(env_vars))
    
    def _analyze_dependencies(self) -> Dict:
        """의존성 분석"""
        dependencies = {
            "external_services": [],
            "third_party_apis": [],
            "security_requirements": []
        }
        
        # Redis, Elasticsearch 등 외부 서비스 감지
        all_files = list(self.repo_path.rglob("*"))
        for file in all_files:
            if file.is_file() and file.suffix in ['.java', '.js', '.py', '.yml', '.properties']:
                try:
                    content = file.read_text().lower()
                    if "redis" in content:
                        dependencies["external_services"].append("redis")
                    if "elasticsearch" in content:
                        dependencies["external_services"].append("elasticsearch")
                    if "kafka" in content:
                        dependencies["external_services"].append("kafka")
                except:
                    continue
        
        # 중복 제거
        dependencies["external_services"] = list(set(dependencies["external_services"]))
        
        return dependencies
    
    def _analyze_build_configuration(self) -> Dict:
        """빌드 설정 분석"""
        build_config = {
            "build_tool": None,
            "java_version": None,
            "node_version": None,
            "docker_required": False
        }
        
        # Maven/Gradle 분석
        if (self.repo_path / "pom.xml").exists():
            build_config["build_tool"] = "maven"
            try:
                pom_content = (self.repo_path / "pom.xml").read_text()
                java_version_match = re.search(r'<java\.version>([^<]+)</java\.version>', pom_content)
                if java_version_match:
                    build_config["java_version"] = java_version_match.group(1)
            except:
                pass
        
        elif (self.repo_path / "build.gradle").exists():
            build_config["build_tool"] = "gradle"
        
        # Node.js 버전 분석
        if (self.repo_path / "package.json").exists():
            try:
                package_json = json.loads((self.repo_path / "package.json").read_text())
                if "engines" in package_json and "node" in package_json["engines"]:
                    build_config["node_version"] = package_json["engines"]["node"]
            except:
                pass
        
        # Dockerfile 존재 여부
        if (self.repo_path / "Dockerfile").exists():
            build_config["docker_required"] = True
        
        return build_config
    
    def generate_summary(self) -> str:
        """분석 결과 요약 생성"""
        if not self.analysis_result:
            self.analyze()
        
        summary = f"""
🔍 Application Analysis Summary
================================

📱 Application Type: {self.analysis_result['app_type']}
🚀 Framework: {self.analysis_result['framework']}
🗄️  Database Required: {self.analysis_result['database']['required']}
🔌 Ports: {', '.join(map(str, self.analysis_result['ports']))}
💾 Memory Limit: {self.analysis_result['resources']['memory_limit']}
🔄 Replicas: {self.analysis_result['resources']['replicas']}
🌍 Environment Variables: {len(self.analysis_result['environment'])}

Recommended Infrastructure:
- EKS Cluster with {self.analysis_result['resources']['replicas']} replicas
- Memory: {self.analysis_result['resources']['memory_limit']} per pod
- CPU: {self.analysis_result['resources']['cpu_limit']} per pod
"""
        
        if self.analysis_result['database']['required']:
            db_type = self.analysis_result['database'].get('type', 'mysql')
            summary += f"- RDS {db_type.upper()} database\n"
        
        return summary

def main():
    """메인 실행 함수"""
    import sys
    
    if len(sys.argv) != 2:
        print("Usage: python code_analyzer.py <repo_path>")
        sys.exit(1)
    
    repo_path = sys.argv[1]
    analyzer = ApplicationAnalyzer(repo_path)
    result = analyzer.analyze()
    
    print(analyzer.generate_summary())
    
    # JSON 결과 저장
    output_file = "analysis_result.json"
    with open(output_file, 'w') as f:
        json.dump(result, f, indent=2)
    
    print(f"\n📄 Detailed analysis saved to: {output_file}")

if __name__ == "__main__":
    main()

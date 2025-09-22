#!/usr/bin/env python3
"""
Complete AI-Driven DevOps Pipeline with K8s Generation
코드 분석 → Terraform → Kubernetes → 배포 자동화
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from analyzer.code_analyzer import ApplicationAnalyzer
from analyzer.report_generator import AnalysisReportGenerator
from generator.terraform_generator import TerraformGenerator
from generator.k8s_generator import KubernetesGenerator
from github.fixed_pr_automation import FixedGitHubPRAutomation
import config

def run_enhanced_pipeline():
    """강화된 완전 자동화 파이프라인"""
    
    print("🤖 Starting Enhanced AI-Driven DevOps Pipeline")
    print("=" * 70)
    
    try:
        # Phase 1: 애플리케이션 분석
        print("\n📋 Phase 1: Application Analysis")
        print("-" * 50)
        
        analyzer = ApplicationAnalyzer(config.APPLICATION_SOURCE_PATH)
        analysis_result = analyzer.analyze()
        
        print(f"✅ Framework: {analysis_result['framework']}")
        print(f"✅ Database: {'Required' if analysis_result['database']['required'] else 'Not required'}")
        print(f"✅ Replicas: {analysis_result['resources']['replicas']}")
        print(f"✅ Memory: {analysis_result['resources']['memory_limit']}")
        
        # Phase 2: 리포트 생성
        print("\n📊 Phase 2: Analysis Report Generation")
        print("-" * 50)
        
        os.makedirs('reports', exist_ok=True)
        report_generator = AnalysisReportGenerator(analysis_result, config.APPLICATION_SOURCE_PATH)
        report_file = report_generator.save_report("./reports")
        
        summary = report_generator.generate_json_summary()
        with open("analysis_summary.json", 'w') as f:
            import json
            json.dump(summary, f, indent=2)
        
        print(f"✅ Report: {report_file}")
        print(f"✅ Summary: analysis_summary.json")
        
        # Phase 3: Terraform 인프라 생성
        print("\n🏗️ Phase 3: Terraform Infrastructure Generation")
        print("-" * 50)
        
        terraform_config = {
            "AWS_REGION": config.AWS_REGION,
            "PROJECT_NAME": config.PROJECT_NAME,
            "ENVIRONMENT": config.ENVIRONMENT,
            "ECR_IMAGE_URI": config.ECR_IMAGE_URI,
            "DOMAIN_NAME": config.DOMAIN_NAME
        }
        
        terraform_generator = TerraformGenerator(analysis_result, terraform_config)
        terraform_files = terraform_generator.generate_all("./generated_terraform")
        
        print(f"✅ Generated {len(terraform_files)} Terraform files")
        
        # Phase 4: Kubernetes 매니페스트 생성
        print("\n☸️ Phase 4: Kubernetes Manifest Generation")
        print("-" * 50)
        
        k8s_config = {
            "PROJECT_NAME": config.PROJECT_NAME,
            "K8S_NAMESPACE": config.K8S_NAMESPACE,
            "ECR_IMAGE_URI": config.ECR_IMAGE_URI,
            "DOMAIN_NAME": config.DOMAIN_NAME,
            "SSL_CERTIFICATE_ARN": config.SSL_CERTIFICATE_ARN
        }
        
        k8s_generator = KubernetesGenerator(analysis_result, k8s_config)
        k8s_files = k8s_generator.generate_all("./generated_k8s")
        
        print(f"✅ Generated {len(k8s_files)} Kubernetes manifests")
        for file_path in k8s_files.values():
            print(f"   📄 {os.path.basename(file_path)}")
        
        # Phase 5: GitHub PR 생성
        print("\n🔄 Phase 5: GitHub PR Creation")
        print("-" * 50)
        
        # 모든 생성된 파일들을 포함
        all_files = {**terraform_files, **k8s_files}
        
        pr_automation = FixedGitHubPRAutomation(analysis_result, all_files)
        pr_url = pr_automation.create_infrastructure_pr()
        
        print(f"✅ PR created: {pr_url}")
        
        # 완료 요약
        print("\n" + "=" * 70)
        print("🎉 ENHANCED PIPELINE EXECUTION COMPLETE!")
        print("=" * 70)
        
        print(f"\n📊 Analysis Summary:")
        print(f"   🎯 Application: {analysis_result['framework']}")
        print(f"   📁 Source: {config.APPLICATION_SOURCE_PATH}")
        print(f"   💾 Memory: {analysis_result['resources']['memory_limit']} per pod")
        print(f"   🔄 Replicas: {analysis_result['resources']['replicas']}")
        print(f"   💰 Est. Cost: ${summary['summary']['estimated_cost']}/month")
        
        print(f"\n🏗️ Generated Infrastructure:")
        print(f"   📄 Terraform files: {len(terraform_files)}")
        print(f"   ☸️ Kubernetes manifests: {len(k8s_files)}")
        print(f"   📊 Analysis report: {report_file}")
        
        print(f"\n🚀 Deployment Pipeline:")
        print(f"   1. ✅ Infrastructure PR: {pr_url}")
        print(f"   2. 🔄 Approve PR → Terraform deploys AWS infrastructure")
        print(f"   3. ☸️ Apply K8s manifests → Deploy application")
        print(f"   4. 🌐 Access via: https://{config.DOMAIN_NAME}")
        
        return {
            "success": True,
            "analysis": analysis_result,
            "report_file": report_file,
            "terraform_files": terraform_files,
            "k8s_files": k8s_files,
            "pr_url": pr_url,
            "summary": summary
        }
        
    except Exception as e:
        print(f"\n❌ Enhanced pipeline failed: {str(e)}")
        return {"success": False, "error": str(e)}

def main():
    """메인 실행 함수"""
    result = run_enhanced_pipeline()
    
    if result["success"]:
        print(f"\n✨ Enhanced AI-Driven DevOps Pipeline completed successfully!")
        print(f"🎯 Ready for complete infrastructure and application deployment!")
        exit(0)
    else:
        print(f"\n💥 Enhanced pipeline execution failed!")
        exit(1)

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Complete AI-Driven DevOps Pipeline
코드 분석 → 리포트 생성 → Terraform 생성 → GitHub PR 자동화
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from analyzer.code_analyzer import ApplicationAnalyzer
from analyzer.report_generator import AnalysisReportGenerator
from generator.terraform_generator import TerraformGenerator
from github.pr_automation import GitHubPRAutomation
import config

def run_complete_pipeline():
    """완전한 AI 기반 DevOps 파이프라인 실행"""
    
    print("🤖 Starting Complete AI-Driven DevOps Pipeline")
    print("=" * 60)
    
    try:
        # Phase 1: 애플리케이션 코드 분석
        print("\n📋 Phase 1: Application Analysis")
        print("-" * 40)
        
        analyzer = ApplicationAnalyzer(config.APPLICATION_SOURCE_PATH)
        analysis_result = analyzer.analyze()
        
        print(f"✅ Application analyzed: {analysis_result['framework']}")
        print(f"✅ Database required: {analysis_result['database']['required']}")
        print(f"✅ Recommended replicas: {analysis_result['resources']['replicas']}")
        
        # Phase 2: 분석 리포트 생성
        print("\n📊 Phase 2: Report Generation")
        print("-" * 40)
        
        report_generator = AnalysisReportGenerator(analysis_result, config.APPLICATION_SOURCE_PATH)
        report_file = report_generator.save_report("./reports")
        
        # JSON 요약 저장
        summary = report_generator.generate_json_summary()
        with open("analysis_summary.json", 'w') as f:
            import json
            json.dump(summary, f, indent=2)
        
        print(f"✅ Analysis report: {report_file}")
        print(f"✅ Summary saved: analysis_summary.json")
        
        # Phase 3: Terraform 코드 생성
        print("\n🏗️ Phase 3: Terraform Code Generation")
        print("-" * 40)
        
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
        for file_path in terraform_files.values():
            print(f"   📄 {file_path}")
        
        # Phase 4: GitHub PR 자동화
        print("\n🔄 Phase 4: GitHub PR Automation")
        print("-" * 40)
        
        pr_automation = GitHubPRAutomation(analysis_result, terraform_files)
        pr_url = pr_automation.create_infrastructure_pr()
        
        print(f"✅ Infrastructure PR created: {pr_url}")
        
        # 완료 요약
        print("\n" + "=" * 60)
        print("🎉 PIPELINE EXECUTION COMPLETE!")
        print("=" * 60)
        
        print(f"\n📊 Summary:")
        print(f"   🎯 Application: {analysis_result['framework']}")
        print(f"   💾 Memory: {analysis_result['resources']['memory_limit']} per pod")
        print(f"   🔄 Replicas: {analysis_result['resources']['replicas']}")
        print(f"   💰 Est. Cost: ${summary['summary']['estimated_cost']}/month")
        
        print(f"\n🔗 Generated Assets:")
        print(f"   📄 Analysis Report: {report_file}")
        print(f"   🏗️ Terraform Code: {len(terraform_files)} files")
        print(f"   🔄 GitHub PR: {pr_url}")
        
        print(f"\n🚀 Next Steps:")
        print(f"   1. Review and approve the GitHub PR")
        print(f"   2. GitHub Actions will deploy infrastructure automatically")
        print(f"   3. EKS cluster will be ready for application deployment")
        print(f"   4. Kubernetes manifests will be generated next")
        
        return {
            "success": True,
            "analysis": analysis_result,
            "report_file": report_file,
            "terraform_files": terraform_files,
            "pr_url": pr_url,
            "summary": summary
        }
        
    except Exception as e:
        print(f"\n❌ Pipeline failed: {str(e)}")
        print(f"🔍 Check logs for detailed error information")
        
        return {
            "success": False,
            "error": str(e)
        }

def main():
    """메인 실행 함수"""
    result = run_complete_pipeline()
    
    if result["success"]:
        print(f"\n✨ AI-Driven DevOps Pipeline completed successfully!")
        exit(0)
    else:
        print(f"\n💥 Pipeline execution failed!")
        exit(1)

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Enhanced Amazon Q Code Analyzer with Report Generation
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from analyzer.code_analyzer import ApplicationAnalyzer
from analyzer.report_generator import AnalysisReportGenerator
from generator.terraform_generator import TerraformGenerator
import config

def main():
    """메인 실행 함수 - 전체 파이프라인"""
    print("🚀 Starting Amazon Q AI-Driven Analysis Pipeline\n")
    
    # 1단계: 코드 분석
    print("📋 Phase 1: Application Code Analysis")
    analyzer = ApplicationAnalyzer(config.APPLICATION_SOURCE_PATH)
    analysis_result = analyzer.analyze()
    
    print(analyzer.generate_summary())
    
    # 2단계: 분석 리포트 생성
    print("\n📊 Phase 2: Generating Analysis Report")
    report_generator = AnalysisReportGenerator(analysis_result, config.APPLICATION_SOURCE_PATH)
    
    # 마크다운 리포트 저장
    report_file = report_generator.save_report("./reports")
    print(f"✅ Detailed report saved: {report_file}")
    
    # JSON 요약 저장
    summary = report_generator.generate_json_summary()
    with open("analysis_summary.json", 'w') as f:
        import json
        json.dump(summary, f, indent=2)
    print("✅ Summary saved: analysis_summary.json")
    
    # 3단계: Terraform 코드 생성
    print("\n🏗️ Phase 3: Generating Terraform Infrastructure Code")
    
    terraform_config = {
        "AWS_REGION": config.AWS_REGION,
        "PROJECT_NAME": config.PROJECT_NAME,
        "ENVIRONMENT": config.ENVIRONMENT,
        "ECR_IMAGE_URI": config.ECR_IMAGE_URI,
        "DOMAIN_NAME": config.DOMAIN_NAME
    }
    
    terraform_generator = TerraformGenerator(analysis_result, terraform_config)
    generated_files = terraform_generator.generate_all("./generated_terraform")
    
    print("✅ Generated Terraform files:")
    for file_path in generated_files.values():
        print(f"   📄 {file_path}")
    
    # 4단계: 다음 단계 안내
    print(f"\n🎯 Next Steps:")
    print("1. Review generated Terraform code")
    print("2. Create GitHub PR for infrastructure")
    print("3. Deploy infrastructure via GitHub Actions")
    print("4. Generate Kubernetes manifests")
    print("5. Deploy application to EKS")
    
    print(f"\n📈 Estimated Monthly Cost: ${summary['summary']['estimated_cost']}")
    print(f"🔄 Recommended Replicas: {summary['summary']['replicas']}")
    print(f"💾 Memory per Pod: {summary['summary']['memory_limit']}")
    
    return {
        "analysis": analysis_result,
        "report": report_file,
        "terraform_files": generated_files,
        "summary": summary
    }

if __name__ == "__main__":
    result = main()

#!/usr/bin/env python3
"""
Infrastructure-Only Pipeline (Phase 1)
코드 분석 → Terraform 생성 → 인프라 PR 생성
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from analyzer.code_analyzer import ApplicationAnalyzer
from analyzer.report_generator import AnalysisReportGenerator
from generator.terraform_generator import TerraformGenerator
from github.fixed_pr_automation import FixedGitHubPRAutomation
import config

def run_infrastructure_pipeline():
    """인프라 전용 파이프라인 (1단계)"""
    
    print("🏗️ Starting Infrastructure-Only Pipeline (Phase 1)")
    print("=" * 60)
    
    try:
        # Phase 1: 애플리케이션 분석
        print("\n📋 Phase 1: Application Analysis")
        print("-" * 40)
        
        analyzer = ApplicationAnalyzer(config.APPLICATION_SOURCE_PATH)
        analysis_result = analyzer.analyze()
        
        print(f"✅ Framework: {analysis_result['framework']}")
        print(f"✅ Database: {'Required' if analysis_result['database']['required'] else 'Not required'}")
        print(f"✅ Replicas: {analysis_result['resources']['replicas']}")
        
        # Phase 2: 분석 리포트 생성
        print("\n📊 Phase 2: Analysis Report")
        print("-" * 40)
        
        os.makedirs('reports', exist_ok=True)
        report_generator = AnalysisReportGenerator(analysis_result, config.APPLICATION_SOURCE_PATH)
        report_file = report_generator.save_report("./reports")
        
        summary = report_generator.generate_json_summary()
        with open("analysis_summary.json", 'w') as f:
            import json
            json.dump(summary, f, indent=2)
        
        print(f"✅ Report saved: {report_file}")
        
        # Phase 3: Terraform 인프라 생성만
        print("\n🏗️ Phase 3: Terraform Infrastructure Generation")
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
        
        # Phase 4: 인프라 PR 생성
        print("\n🔄 Phase 4: Infrastructure PR Creation")
        print("-" * 40)
        
        # 커스텀 PR 생성 (인프라 전용)
        pr_url = create_infrastructure_pr(analysis_result, terraform_files)
        
        print(f"✅ Infrastructure PR created: {pr_url}")
        
        # 완료 요약
        print("\n" + "=" * 60)
        print("🎉 INFRASTRUCTURE PIPELINE COMPLETE!")
        print("=" * 60)
        
        print(f"\n📊 Analysis Results:")
        print(f"   🎯 Application: {analysis_result['framework']}")
        print(f"   💾 Memory: {analysis_result['resources']['memory_limit']} per pod")
        print(f"   🔄 Replicas: {analysis_result['resources']['replicas']}")
        print(f"   💰 Est. Cost: ${summary['summary']['estimated_cost']}/month")
        
        print(f"\n🏗️ Generated Infrastructure:")
        print(f"   📄 Terraform files: {len(terraform_files)}")
        print(f"   📊 Analysis report: {report_file}")
        
        print(f"\n🚀 Next Steps:")
        print(f"   1. ✅ Review Infrastructure PR: {pr_url}")
        print(f"   2. 👨‍💼 Admin approves PR")
        print(f"   3. 🏗️ GitHub Actions deploys AWS infrastructure")
        print(f"   4. ☸️ Phase 2: K8s deployment pipeline will be triggered")
        
        return {
            "success": True,
            "analysis": analysis_result,
            "terraform_files": terraform_files,
            "pr_url": pr_url,
            "summary": summary
        }
        
    except Exception as e:
        print(f"\n❌ Infrastructure pipeline failed: {str(e)}")
        return {"success": False, "error": str(e)}

def create_infrastructure_pr(analysis_result, terraform_files):
    """인프라 전용 PR 생성"""
    import subprocess
    from datetime import datetime
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    branch_name = f"infrastructure/phase1-{timestamp}"
    
    # Git 설정
    subprocess.run(["git", "config", "--global", "user.name", "Amazon Q AI"], check=True)
    subprocess.run(["git", "config", "--global", "user.email", "ai@amazonq.aws"], check=True)
    
    # 브랜치 생성
    subprocess.run(["git", "checkout", "dev"], check=True)
    subprocess.run(["git", "pull", "origin", "dev"], check=True)
    subprocess.run(["git", "checkout", "-b", branch_name], check=True)
    
    # Terraform 파일 정리
    os.makedirs("terraform", exist_ok=True)
    if os.path.exists("generated_terraform"):
        subprocess.run(["cp", "-r", "generated_terraform/.", "terraform/"], check=True)
    
    # 변경사항 커밋
    subprocess.run(["git", "add", "terraform/", "reports/", "analysis_summary.json"], check=True)
    
    commit_msg = f"""🏗️ Phase 1: AWS Infrastructure Generation

🤖 AI Analysis Results:
- Framework: {analysis_result['framework']}
- Database: {'Required' if analysis_result['database']['required'] else 'Not required'}
- Replicas: {analysis_result['resources']['replicas']}
- Memory: {analysis_result['resources']['memory_limit']}

🏗️ Generated AWS Infrastructure:
- VPC with Multi-AZ subnets
- EKS Kubernetes cluster
- RDS database (if required)
- Security groups and IAM roles

💰 Estimated Cost: ~$200-250/month

🚀 Deployment Process:
1. Review Terraform code in terraform/ directory
2. Approve this PR to deploy AWS infrastructure
3. GitHub Actions will create EKS cluster
4. Phase 2 (K8s deployment) will follow

Generated by Amazon Q AI - Phase 1 Infrastructure"""
    
    subprocess.run(["git", "commit", "-m", commit_msg], check=True)
    subprocess.run(["git", "push", "origin", branch_name], check=True)
    
    # PR 생성
    pr_title = "🏗️ Phase 1: AWS Infrastructure Deployment"
    pr_body = f"""## 🏗️ Phase 1: AWS Infrastructure Deployment

**AI Analysis Engine**: Amazon Q Code Analyzer  
**Framework Detected**: {analysis_result['framework']}  
**Deployment Phase**: Infrastructure Only (Phase 1)  

### 📊 Application Analysis
- **Framework**: {analysis_result['framework']}
- **Database Required**: {'✅ Yes (MySQL)' if analysis_result['database']['required'] else '❌ No'}
- **Memory per Pod**: {analysis_result['resources']['memory_limit']}
- **Recommended Replicas**: {analysis_result['resources']['replicas']}

### 🏗️ AWS Infrastructure Components
- **VPC**: Multi-AZ with public/private subnets
- **EKS Cluster**: Kubernetes cluster ready for applications
- **RDS Database**: {'MySQL database with backup' if analysis_result['database']['required'] else 'No database required'}
- **Security**: IAM roles and security groups
- **Networking**: Load balancer and routing

### 💰 Cost Estimation
- **Monthly Total**: ~$200-250
- **EKS Cluster**: $73/month
- **Worker Nodes**: $90/month (auto-scaling)
- **RDS**: {'$25/month' if analysis_result['database']['required'] else '$0/month'}

### 🚀 Deployment Process

#### ✅ This PR (Phase 1)
1. **Review** Terraform code in `terraform/` directory
2. **Approve** this PR to deploy AWS infrastructure
3. **GitHub Actions** will automatically deploy EKS cluster
4. **Verify** infrastructure is ready

#### 🔄 Next Phase (Phase 2)
1. **Automatic trigger** after infrastructure deployment
2. **K8s manifests** will be generated
3. **Application deployment PR** will be created
4. **Final approval** for application deployment

### 📋 What's Included
- `terraform/main.tf` - Main infrastructure configuration
- `terraform/modules/` - VPC, EKS, RDS modules
- `reports/` - Detailed AI analysis report
- `analysis_summary.json` - Machine-readable summary

### 🔒 Security & Best Practices
- ✅ Private subnets for application workloads
- ✅ IAM roles with least privilege
- ✅ Encryption at rest and in transit
- ✅ Multi-AZ deployment for high availability

---

### 🤖 AI Automation - Phase 1
This is **Phase 1** of the AI-driven deployment pipeline. After this infrastructure is deployed, **Phase 2** will automatically generate Kubernetes manifests and create a second PR for application deployment.

**Ready for infrastructure deployment!** 🚀"""
    
    result = subprocess.run([
        "gh", "pr", "create",
        "--title", pr_title,
        "--body", pr_body,
        "--base", "dev",
        "--head", branch_name,
        "--label", "phase-1,infrastructure,ai-generated"
    ], capture_output=True, text=True, check=True)
    
    return result.stdout.strip()

def main():
    """메인 실행 함수"""
    result = run_infrastructure_pipeline()
    
    if result["success"]:
        print(f"\n✨ Phase 1 Infrastructure Pipeline completed!")
        exit(0)
    else:
        print(f"\n💥 Phase 1 Pipeline failed!")
        exit(1)

if __name__ == "__main__":
    main()

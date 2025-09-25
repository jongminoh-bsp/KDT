terraform {
  backend "s3" {
    bucket = "kdt-project-terraform-state"
    key    = "skyline/terraform.tfstate"
    region = "ap-northeast-2"
  }
}

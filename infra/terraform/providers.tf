provider "aws" {
  region     = var.aws_region
  profile    = var.aws_profile                          # Ton profil AWS configuré
  endpoints {
    s3 = var.aws_s3_endpoint
  }

  skip_credentials_validation = true            # ✅ Important: MinIO doesn't need AWS IAM validation
  skip_metadata_api_check     = true            # ✅ Important: No metadata API like on EC2
  skip_requesting_account_id  = true            # ✅ Important: No request for account ID
  skip_region_validation      = true            # ✅ Important: No region validation



  default_tags {
    tags = local.common_tags
  }
}

provider "minio" {
  minio_server   = var.minio_server
  minio_user     = var.minio_user
  minio_password = var.minio_password
  minio_region   = var.minio_region
  minio_ssl      = false
}

provider "kubernetes" {
  config_path = "~/.kube/config"
  config_context = "k3d-local-hydrosat-cluster"
}

provider "helm" {
  kubernetes {
    config_path = "~/.kube/config"
    config_context = "k3d-local-hydrosat-cluster"
  }
}

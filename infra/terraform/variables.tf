variable "aws_account_id" {
  type        = string
  description = "Target AWS acccount ID"
}

variable "aws_region" {
  type        = string
  description = "Target AWS region"
}

variable "aws_profile" {
  type        = string
  description = "AWS profile"
}

variable "aws_s3_endpoint" {
  type        = string
  description = "AWS S3 endpoint"
}

variable "environment" {
  type        = string
  description = "Environment name (local, dev, staging, prod)"
}

variable "creator" {
  type        = string
  description = "$USER of the user that will deploy the infrastructure using terraform apply"
}

variable "workspace" {
  type        = string
  description = "Workspace name"
}

variable "service_name" {
  type        = string
  description = "Service name"
  default     = "poc-recruitment-exercise"
}

variable "minio_server" {
  description = "Adresse of the MinIO server"
  type        = string
}

variable "minio_user" {
  description = "MinIO user"
  type        = string
}

variable "minio_password" {
  description = "MinIO password"
  type        = string
}

variable "minio_region" {
  description = "MinIO region"
  type        = string
}

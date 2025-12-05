variable "aws_region" {
  description = "AWS Region (Stockholm)"
  type        = string
  default     = "eu-north-1"
}

variable "project_name" {
  description = "Project name prefix"
  type        = string
  default     = "coretelecoms-capstone"
}

variable "environment" {
  default = "prod"
}

variable "create_instance" {
  default = "false"
}

variable "gcp_region" {
  description = "GCP Region (US)"
  type        = string
  default     = "us-central1"
}

variable "gcp_projectid" {
  description = "Project"
  type        = string
  default     = "onyx-cosmos-480018-k1"
}

variable "credentials" {
  description = "My Credentials"
  default     = "~/.google/creds/coretelecoms.json"
}

variable "location" {
  description = "Project Location"
  type        = string
  default     = "US"
}

variable "gcs_storage_class" {
  description = "Bucket Storage Class"
  default     = "STANDARD"
}

variable "bigquery_dataset_id" {
  description = "My BigQuery Dataset Name"
  #Update the below to what you want your dataset to be called
  default     = "coretelecoms_capstone_datawarehouse"
}
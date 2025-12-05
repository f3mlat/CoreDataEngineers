terraform {
  # The required_providers block specifies provider sources and versions
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.0"
    }

    google = {
      source  = "hashicorp/google"
      version = "~> 7.0"
    }
  }

  # The backend block is separate and configures state storage
  backend "s3" {
    bucket = "coretelecoms-capstone-terraform-state"
    key    = "terraform.tfstate"
    region = "eu-north-1"
  }
}

provider "aws" {
  region = var.aws_region
}

provider "google" {
  credentials = file(var.credentials)
  project     = var.gcp_projectid
  region      = var.gcp_region
}
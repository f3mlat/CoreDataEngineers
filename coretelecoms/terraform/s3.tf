resource "aws_s3_bucket" "terraform_state_bucket" {
  bucket = "${var.project_name}-terraform-state"

  tags = {
    Name        = "CoreTelecomsTerraformStateBucket"
    Environment = var.environment
  }
}

resource "aws_s3_bucket_versioning" "terraform_state_bucket_versioning" {
  bucket = aws_s3_bucket.terraform_state_bucket.id
  versioning_configuration {
    status = "Enabled"
  }
}
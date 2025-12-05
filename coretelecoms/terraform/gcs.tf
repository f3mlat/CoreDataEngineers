resource "google_storage_bucket" "datalake" {
  name          = "${var.project_name}-datalake"
  location      = var.location
  force_destroy = true


  lifecycle_rule {
    condition {
      age = 1
    }
    action {
      type = "AbortIncompleteMultipartUpload"
    }
  }
}

resource "google_bigquery_dataset" "datawarehouse" {
  dataset_id = var.bigquery_dataset_id
  location   = var.location
}
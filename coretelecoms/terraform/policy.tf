#data "aws_iam_policy_document" "s3_write_policy_document" {
#  statement {
#    effect = "Allow"
#
#    actions = [
#      "s3:ListBucket",
#      "s3:GetObject",
#      "s3:PutObject",
#      "s3:DeleteObject"
#    ]
#
#    resources = [
#      aws_s3_bucket.datalake.arn,
#      "${aws_s3_bucket.datalake.arn}/*"
#    ]
#  }
#}
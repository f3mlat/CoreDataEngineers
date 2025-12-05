#data "aws_iam_user" "capstone_user" {
#  user_name = "CDE_Lateef_Akinola_3"
#}
#
#resource "aws_iam_policy" "capstone_s3_policy" {
#  name        = "CoreTelecomsCapstoneS3Access"
#  description = "A policy granting read and write access of an S3 bucket to capstone user."
#  policy      = data.aws_iam_policy_document.s3_write_policy_document.json
#}
#
#resource "aws_iam_user_policy_attachment" "attach_s3" {
#  user       = data.aws_iam_user.capstone_user.user_name
#  policy_arn = aws_iam_policy.capstone_s3_policy.arn
#}
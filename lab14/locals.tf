locals {
  common_tags = {
    itclass = var.itclass
    itgroup = var.itgroup
  }

  cName = var.cName

  s3_bucket_name = "${var.bucket_name_prefix}-${var.cName}-${random_integer.rand.result}"
}
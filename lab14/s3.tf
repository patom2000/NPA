##################################################################################
# RESOURCES
##################################################################################

#Random ID
resource "random_integer" "rand" {
  min = 100
  max = 99999
}

resource "aws_s3_bucket" "web_bucket" {
    bucket        = local.s3_bucket_name
    force_destroy = true

    tags = merge(local.common_tags, { Name = "${var.cName}-web-bucket" })

  }
resource "aws_s3_bucket_object" "object1" {
  bucket = aws_s3_bucket.web_bucket.bucket
  key = "index.html" #ตั้งอะไรก็ได้
  source = "./website/index.html"
}

resource "aws_s3_bucket_object" "object2" {
  bucket = aws_s3_bucket.web_bucket.bucket
  key = "holy patom"
  source = "./website/holypatom.png"
}

resource "aws_s3_bucket_acl" "exacl"{
  bucket = aws_s3_bucket.web_bucket.id
  acl = "private"
}
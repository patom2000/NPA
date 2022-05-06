

resource "aws_s3_bucket" "web_bucket" {
  bucket        = var.bucket_name
  acl           = "private"
  force_destroy = true

 

  tags = merge(var.common_tags, { Name = "${var.addName}-web-bucket" })

}


##################################################################################
# RESOURCES
##################################################################################

#Random ID
resource "random_integer" "rand" {
  min = 100
  max = 99999
}

module "my_s3_bucket" {
  source = "./module/my-s3"

  bucket_name = local.s3_bucket_name
  common_tags = local.common_tags
  addName = local.cName
}

resource "aws_s3_bucket_object" "website" {
  bucket = module.my_s3_bucket.web_bucket.id
  key    = "index.html"
  source = "./website/index.html"

  tags = local.common_tags

}

resource "aws_s3_bucket_object" "graphic" {
  bucket = module.my_s3_bucket.web_bucket.id
  key    = "Globo_logo_Vert.png"
  source = "./website/Globo_logo_Vert.png"

  tags = local.common_tags

}
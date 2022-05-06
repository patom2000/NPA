variable "bucket_name" {
  type = string
  description =" bucket name for my s3 module"
}
variable "common_tags" {
  type = map(string)
  description = "map of tag to be apply to my s3 module"
}
variable "addName" {
  type = string
  description = "common name for tagging in my s3 module"
}
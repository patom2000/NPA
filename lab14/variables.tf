##################################################################################
# VARIABLES
##################################################################################

variable "aws_access_key" {
    type        = string
    description = "AWS Access Key"
    sensitive   = true
}
variable "aws_secret_key" {
    type        = string
    description = "AWS Secret Key"
    sensitive   = true
}
variable "aws_session_token" {
    type        = string
    description = "AWS Session Token"
    sensitive   = true
}
variable "private_key_path" {
    type        = string
    description = "Private key path"
    sensitive   = true
}
variable "key_name" {
    type        = string
    description = "Private key path"
    sensitive   = false
}
variable "region" {
    type        = string
    description = "value for default region"
     default = "us-east-1"
}

variable "enable_dns_hostnames" {
    type        = bool
    description = "Enable DNS hostnames in VPC"
    default     = true
}


variable "network_address_space" {
    type        = string
    description = "Base CIDR Block for VPC"
    default = "10.0.0.0/16"
}


variable "instance_count" {
  type = number
  description = "number of instance"
  default = 2
}

variable "subnet_count" {
    type = number
    description = "number of subnet"
    default = 2
}

variable "bucket_name_prefix" {
    type        = string
    description = "Prefix for S3 bucket"
    default     = "npa22bucket"
}
  
variable "cName" {
    type        = string
    description = "Common name for tagging"
    default = "ITKMITL"    
}
  
variable "itclass" {
    type        = string
    description = "Class name for tagging"
}

variable "itgroup" {
    type        = string
    description = "Group number for tagging"
}
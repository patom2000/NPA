##################################################################################
# VARIABLES
##################################################################################

variable "aws_access_key" {}
variable "aws_secret_key" {}
variable "aws_session_token" {}
variable "private_key_path" {}
variable "key_name" {}
variable "region" {
  default = "us-east-1"
}
variable "network_address_space" {
  default = "10.0.0.0/16"
}
variable "subnet1_address_space" {
  default = "10.0.1.0/24"
}
variable "subnet2_address_space" {
    default = "10.0.2.0/24"
}
variable "bucket_name_prefix" {}
variable "itclass" {}
variable "itgroup" {}
variable "cName" {}

##################################################################################
# PROVIDERS
##################################################################################

provider "aws" {
  access_key = var.aws_access_key
  secret_key = var.aws_secret_key
  region     = var.region
  token = var.aws_session_token
}

##################################################################################
# LOCALS
##################################################################################

locals {
  common_tags = {
    itclass = var.itclass
    itgroup = var.itgroup
  }

  cName = var.cName
  s3_bucket_name = "${var.bucket_name_prefix}-${var.cName}-${random_integer.rand.result}"
}

##################################################################################
# DATA
##################################################################################
data "aws_availability_zones" "available" {}

data "aws_ami" "aws-linux" {
  most_recent = true
  owners      = ["amazon"]

  filter {
    name   = "name"
    values = ["amzn-ami-hvm*"]
  }

  filter {
    name   = "root-device-type"
    values = ["ebs"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
}


##################################################################################
# RESOURCES
##################################################################################

#Random ID
resource "random_integer" "rand" {
  min = 100
  max = 99999
}

resource "aws_vpc" "testVPC" {
    cidr_block = var.network_address_space
    enable_dns_hostnames = true

    tags = merge(local.common_tags, { Name = "${var.cName}-VPC"})
}

resource "aws_subnet" "Public1" {
    vpc_id = aws_vpc.testVPC.id
    cidr_block = var.subnet1_address_space
    availability_zone = data.aws_availability_zones.available.names[0]
    map_public_ip_on_launch = true
    tags = merge(local.common_tags, { Name = "${var.cName}-Public1"})
}

resource "aws_subnet" "Public2" {
    vpc_id = aws_vpc.testVPC.id
    cidr_block = var.subnet2_address_space
    map_public_ip_on_launch = true
    availability_zone = data.aws_availability_zones.available.names[1]

    tags = merge(local.common_tags, { Name = "${var.cName}-Public2"})
}

resource "aws_internet_gateway" "testIgw" {
    vpc_id = aws_vpc.testVPC.id

    tags = merge(local.common_tags, { Name = "${var.cName}-igw"})
}

resource "aws_route_table" "publicRoute" {
    vpc_id = aws_vpc.testVPC.id
        route {
            cidr_block = "0.0.0.0/0"
            gateway_id = aws_internet_gateway.testIgw.id
        }
    tags = merge(local.common_tags, { Name = "${var.cName}-publicRoute"})
}

resource "aws_route_table_association" "rt-pubsub1" {
  subnet_id = aws_subnet.Public1.id
  route_table_id = aws_route_table.publicRoute.id
}

resource "aws_route_table_association" "rt-pubsub2" {
  subnet_id = aws_subnet.Public2.id
  route_table_id = aws_route_table.publicRoute.id
}

resource "aws_security_group" "lb-sg" {
    name = "elb-sg"
    vpc_id = aws_vpc.testVPC.id

    ingress {
        from_port = 80
        to_port = 80
        protocol = "tcp"
        cidr_blocks = ["0.0.0.0/0"]

    }

    egress {
        from_port = 0
        to_port = 0
        protocol = "-1"
        cidr_blocks = ["0.0.0.0/0"]
    }

    tags = merge(local.common_tags, { Name = "${var.cName}-elbsg"})
}

resource "aws_security_group" "allow_ssh_web" {
  name        = "npaWk11_demo"
  description = "Allow ssh and web access"
  vpc_id      = aws_vpc.testVPC.id

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = [var.network_address_space]
  }
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = -1
    cidr_blocks = ["0.0.0.0/0"]
  }
  tags = merge(local.common_tags, { Name = "${var.cName}-securitygroup"})
}

resource "aws_lb" "webLb" {
  name               = "test-lb-tf"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.allow_ssh_web.id]
  subnets            = [aws_subnet.Public1.id, aws_subnet.Public2.id]

  tags = merge(local.common_tags, { Name = "${var.cName}-webLB"})
  
}

resource "aws_lb_target_group" "webTg" {
  name     = "tf-example-lb-tg"
  port     = 80
  protocol = "HTTP"
  vpc_id   = aws_vpc.testVPC.id
  tags = merge(local.common_tags, { Name = "${var.cName}-tg"})
}

resource "aws_lb_listener" "webLs" {
  load_balancer_arn = aws_lb.webLb.arn
  port              = "80"
  protocol          = "HTTP"
  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.webTg.arn
  }
  tags = merge(local.common_tags, { Name = "${var.cName}-ls"})
}

resource "aws_lb_target_group_attachment" "testIst" {
  target_group_arn = aws_lb_target_group.webTg.arn
  target_id        = aws_instance.Server1.id
  port             = 80
}


resource "aws_instance" "Server1" {
  ami                    = data.aws_ami.aws-linux.id
  instance_type          = "t2.micro"
  key_name               = var.key_name
  vpc_security_group_ids = [aws_security_group.allow_ssh_web.id]
  subnet_id = aws_subnet.Public1.id
  connection {
    type        = "ssh"
    host        = self.public_ip
    user        = "ec2-user"
    private_key = file(var.private_key_path)

  }

  provisioner "remote-exec" {
    inline = [
      "sudo yum install nginx -y",
      "sudo service nginx start",
      "sudo rm /usr/share/nginx/html/index.html",
      "echo '<html><head><title>Blue Team Server</title></head><body style=\"background-color:#1F778D\"><p style=\"text-align: center;\"><span style=\"color:#FFFFFF;\"><span style=\"font-size:28px;\">Blue Team</span></span></p></body></html>' | sudo tee /usr/share/nginx/html/index.html"
    ]
  }
  tags = merge(local.common_tags, { Name = "${var.cName}-server1"})
}

resource "aws_instance" "Server2" {
  ami                    = data.aws_ami.aws-linux.id
  instance_type          = "t2.micro"
  key_name               = var.key_name
  vpc_security_group_ids = [aws_security_group.allow_ssh_web.id]
  subnet_id = aws_subnet.Public2.id
  connection {
    type        = "ssh"
    host        = self.public_ip
    user        = "ec2-user"
    private_key = file(var.private_key_path)

  }

  provisioner "remote-exec" {
    inline = [
      "sudo yum install nginx -y",
      "sudo service nginx start",
      "sudo rm /usr/share/nginx/html/index.html",
      "echo '<html><head><title>Green Team Server</title></head><body style=\"background-color:#77A032\"><p style=\"text-align: center;\"><span style=\"color:#FFFFFF;\"><span style=\"font-size:28px;\">Green Team</span></span></p></body></html>' | sudo tee /usr/share/nginx/html/index.html"
    ]
  }
  tags = merge(local.common_tags, { Name = "${var.cName}-server2"})
}

resource "aws_s3_bucket" "web_bucket" {
    bucket        = local.s3_bucket_name
    acl           = "private"
    force_destroy = true

    tags = merge(local.common_tags, { Name = "${var.cName}-web-bucket" })

  }

##################################################################################
# OUTPUT
##################################################################################

output "aws_lb_public_dns" {
  value = aws_lb.webLb.dns_name
}
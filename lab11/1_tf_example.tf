##################################################################################
# PROVIDERS
##################################################################################

provider "aws" {
  access_key = "ASIA6OE7TGF26M35QP5L"
  secret_key = "k4lxB/O2v9x8RxkRmxiUwmM+iu1M68QeEW5Xrol2"
  token = "FwoGZXIvYXdzELn//////////wEaDEpEYwNsCl42oQBE5iLFAUYVokNiQSATe7DuUTHGEGio7fZDqWXVbrZdcXD2xhI5ZlYLXCKhlTlhfWfP/x1Cdvyn+2ybQesvnljelRpcWZH8ukvDJp0tIyYVDe9z+Ba+4heKs4ZUkwOTjMb8aM2lsMLPyONZ5ky9M6gplphUDKeqvjqEHIU4TnHuqtTLmNftSLOJCNV/HHM2aSZ8R2fkTlXLJogx4H5x9ISiqv/n7ZlJHb5BxIiq8u0yyy+E2CExqNrt+DkzE6N3s6eD28sw42NLRAijKNr9n5IGMi2IRiw8Y3BK1utc6erqTFwMgRky0RSXluHKFShyeQ13JC3mehM29TQuFgDZlRQ="
  region     = "us-east-1"
}

##################################################################################
# DATA
##################################################################################

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
    name   = "virtualization-ty
    pe"
    values = ["hvm"]
  }
}


##################################################################################
# RESOURCES
##################################################################################

#This uses the default VPC.  It WILL NOT delete it on destroy.
resource "aws_default_vpc" "default" {

}

resource "aws_security_group" "allow_ssh_web" {
  name        = "npaWk11_demo"
  description = "Allow ssh and web access"
  vpc_id      = aws_default_vpc.default.id

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
    cidr_blocks = ["0.0.0.0/0"]
  }
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = -1
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_instance" "testweb" {
  ami                    = data.aws_ami.aws-linux.id
  instance_type          = "t2.micro"
  key_name               = "vockey"
  vpc_security_group_ids = [aws_security_group.allow_ssh_web.id]

  connection {
    type        = "ssh"
    host        = self.public_ip
    user        = "ec2-user"
    private_key = file("/home/oem/Downloads/labsuser.pem")

  }

  provisioner "remote-exec" {
    inline = [
      "sudo yum install -y httpd mysql php",
      "sudo wget https://aws-tc-largeobjects.s3.amazonaws.com/AWS-TC-AcademyACF/acf-lab3-vpc/lab-app.zip",
      "sudo unzip lab-app.zip -d /var/www/html/",
      "sudo chkconfig httpd on",
      "sudo service httpd start\n"
    ]
  }
}

##################################################################################
# OUTPUT
##################################################################################

output "aws_instance_public_dns" {
  value = aws_instance.testweb.public_dns
}
##################################################################################
# PROVIDERS
##################################################################################

provider "aws" {
  access_key = ""
  secret_key = ""
  token = ""
  region = "us-east-1"
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
    name   = "virtualization-type"
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
    private_key = file("D:/all_work/NPA/NPA/lab11/key/labsuser.pem")

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
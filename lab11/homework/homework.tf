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

resource "aws_vpc" "testVPC" {
    cidr_block = "10.0.0.0/16"
     tags = {
      "Name" = "testVPC"
    }
}
resource "aws_internet_gateway" "igw" {
    vpc_id = aws_vpc.testVPC.id
}

resource "aws_route_table" "testVPC_rt" {
  vpc_id = aws_vpc.testVPC.id
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.igw.id
  }

  tags = {
    Name = "testVPC_rt"
  }
}

resource "aws_subnet" "Public1" {
    vpc_id     = aws_vpc.testVPC.id
    cidr_block = "10.0.1.0/24"
    map_public_ip_on_launch = true

    availability_zone = "us-east-1b"
}

resource "aws_main_route_table_association" "a" {
  vpc_id         = aws_vpc.testVPC.id
  route_table_id = aws_route_table.testVPC_rt.id
}

resource "aws_security_group" "allow_ssh_web" {
  name        = "AllowSSHWeb"
  description = "Allow incoming SSH and HTTP traffic to EC@ Instance"
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
    cidr_blocks = ["0.0.0.0/0"]
  }
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = -1
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_instance" "tfTest" {
    ami                    = data.aws_ami.aws-linux.id
    instance_type          = "t2.micro"
    key_name               = "vockey"
    security_groups = [ aws_security_group.allow_ssh_web.id ]
    subnet_id = aws_subnet.Public1.id
    tags = {
      "Name" = "tfTest"
    }

    root_block_device {
      volume_type = "gp2"
      volume_size = 8
    }

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
  value = aws_instance.tfTest.public_dns
}
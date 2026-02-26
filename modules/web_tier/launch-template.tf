data "aws_ami" "ubuntu" {
  most_recent = true
  owners      = ["099720109477"]

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
}


resource "aws_launch_template" "web_lt" {

  name = "web-launch-template"

  image_id      = data.aws_ami.ubuntu.id
  instance_type = "t3.micro"

  key_name = var.key_name

  vpc_security_group_ids = [
    var.security_group_id
  ]

  user_data = base64encode(<<EOF
#!/bin/bash

apt update -y
apt install -y docker.io -y

systemctl start docker
systemctl enable docker

docker run -d \
-p 8000:8000 \
-e DATABASE_HOST=${var.rds_endpoint} \
-e DATABASE_PORT=3306 \
-e REDIS_HOST=${var.redis_endpoint} \
-e REDIS_PORT=6379 \
nginx
EOF
  )

  tag_specifications {
    resource_type = "instance"

    tags = {
      Name = "web-server"
    }
  }
}

data "aws_ami" "ubuntu" {
  most_recent = true

  owners = ["099720109477"]

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*"]
  }
}

resource "aws_launch_template" "web_lt" {

  name = "web-launch-template"

  image_id      = data.aws_ami.ubuntu.id
  instance_type = "t3.micro"

  key_name = var.key_name

  iam_instance_profile {
    name = var.iam_profile_name
  }

  vpc_security_group_ids = [
    var.security_group_id
  ]

  user_data = base64encode(<<EOF
#!/bin/bash

apt update -y
apt install -y awscli docker.io -y

systemctl enable docker
systemctl start docker

# S3 env 다운로드
aws s3 cp s3://your-web-bucket-name/.env /home/ubuntu/.env

# 환경변수 로드
if [ -f /home/ubuntu/.env ]; then
    export $(cat /home/ubuntu/.env | xargs)
fi

# 기존 컨테이너 정리
docker ps -q | xargs -r docker stop
docker ps -q | xargs -r docker rm

# nginx 실행 (예시)
docker run -d -p 8000:8000 --env-file /home/ubuntu/.env nginx

EOF
)

  tag_specifications {
    resource_type = "instance"

    tags = {
      Name = "web-server"
    }
  }
}

# Amazon Linux 2 최신 AMI 가져오기
data "aws_ami" "amazon_linux_2" {
  most_recent = true
  owners      = ["amazon"]

  filter {
    name   = "name"
    values = ["amzn2-ami-hvm-*-x86_64-gp2"]
  }
}

# 1. SSM 접속을 위한 IAM Role 생성
resource "aws_iam_role" "bastion_role" {
  name = "hisubtory-bastion-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Sid    = ""
        Principal = {
          Service = "ec2.amazonaws.com"
        }
      },
    ]
  })
}

# 2. SSM Managed Instance Core 정책 연결 (SSM 접속 필수 권한)
resource "aws_iam_role_policy_attachment" "bastion_ssm_policy" {
  role       = aws_iam_role.bastion_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore"
}

# 3. 인스턴스 프로파일 생성 (EC2에 Role 연결용)
resource "aws_iam_instance_profile" "bastion_profile" {
  name = "hisubtory-bastion-profile"
  role = aws_iam_role.bastion_role.name
}

# 4. 배스천 EC2 인스턴스 생성
resource "aws_instance" "bastion" {
  ami           = data.aws_ami.amazon_linux_2.id
  instance_type = var.instance_type
  key_name      = var.key_name

  subnet_id                   = var.public_subnet_id
  vpc_security_group_ids      = [var.bastion_sg_id]
  associate_public_ip_address = true

  iam_instance_profile = aws_iam_instance_profile.bastion_profile.name

  tags = {
    Name = "hisubtory-bastion"
  }
}

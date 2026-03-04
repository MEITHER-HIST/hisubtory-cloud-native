data "aws_ami" "ubuntu" {
  most_recent = true
  owners      = ["099720109477"]

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*"]
  }
}

############################
# IAM Role + Instance Profile
############################

resource "aws_iam_role" "bastion_role" {
  name = "bastion-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Principal = {
        Service = "ec2.amazonaws.com"
      }
      Action = "sts:AssumeRole"
    }]
  })
}

resource "aws_iam_instance_profile" "bastion_profile" {
  name = "bastion-profile"
  role = aws_iam_role.bastion_role.name
}

############################
# Bastion EC2
############################

resource "aws_instance" "bastion" {
  ami           = data.aws_ami.ubuntu.id
  instance_type = "t3.micro"

  subnet_id = var.public_subnet_id
  key_name  = var.key_name

  vpc_security_group_ids = [var.bastion_sg_id]

  associate_public_ip_address = true

  iam_instance_profile = aws_iam_instance_profile.bastion_profile.name

  tags = {
    Name = "bastion-server"
  }
}

resource "aws_iam_role_policy" "bastion_s3_policy" {
  name = "bastion-s3-read-policy"
  role = aws_iam_role.bastion_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "s3:GetObject",
          "s3:ListBucket"
        ]
        Resource = [
          "arn:aws:s3:::your-web-bucket-name",
          "arn:aws:s3:::your-web-bucket-name/*"
        ]
      }
    ]
  })
}

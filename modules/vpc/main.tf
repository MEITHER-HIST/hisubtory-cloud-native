# VPC 생성 (전체 네트워크 영역)
resource "aws_vpc" "main" {
  cidr_block = var.vpc_cidr

  tags = {
    Name = "${var.project_name}-vpc"
  }
}

# Public Subnet (인터넷 접근 가능 영역) - AZ-a
resource "aws_subnet" "public_a" {
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.0.1.0/24"
  availability_zone = "ap-northeast-2a"

  tags = {
    Name = "${var.project_name}-public-a"
  }
}

# Public Subnet (인터넷 접근 가능 영역) - AZ-c
resource "aws_subnet" "public_c" {
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.0.2.0/24"
  availability_zone = "ap-northeast-2c"

  tags = {
    Name = "${var.project_name}-public-c"
  }
}

# Private Subnet (내부 서비스 영역) - AZ-a
resource "aws_subnet" "private_a" {
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.0.3.0/24"
  availability_zone = "ap-northeast-2a"

  tags = {
    Name = "${var.project_name}-private-a"
  }
}

# Private Subnet (내부 서비스 영역) - AZ-c
resource "aws_subnet" "private_c" {
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.0.4.0/24"
  availability_zone = "ap-northeast-2c"

  tags = {
    Name = "${var.project_name}-private-c"
  }
}

# Private Data Subnet (DB/Redis 전용 영역) - AZ-a
resource "aws_subnet" "data_a" {
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.0.5.0/24"
  availability_zone = "ap-northeast-2a"

  tags = {
    Name = "${var.project_name}-data-a"
  }
}

# Private Data Subnet (DB/Redis 전용 영역) - AZ-c
resource "aws_subnet" "data_c" {
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.0.6.0/24"
  availability_zone = "ap-northeast-2c"

  tags = {
    Name = "${var.project_name}-data-c"
  }
}

# Internet Gateway (외부 인터넷 연결)
resource "aws_internet_gateway" "igw" {
  vpc_id = aws_vpc.main.id
}

# NAT Gateway용 Elastic IP
resource "aws_eip" "nat" {}

# NAT Gateway (Private → 인터넷 접근용)
resource "aws_nat_gateway" "nat" {
  allocation_id = aws_eip.nat.id
  subnet_id     = aws_subnet.public_a.id
}

# Public Route Table (인터넷 라우팅 설정)
resource "aws_route_table" "public" {
  vpc_id = aws_vpc.main.id
}

# Public Route (인터넷 트래픽 허용)
resource "aws_route" "public_route" {
  route_table_id         = aws_route_table.public.id
  gateway_id             = aws_internet_gateway.igw.id
  destination_cidr_block = "0.0.0.0/0"
}

# Public Subnet Route Table 연결
resource "aws_route_table_association" "public_a_assoc" {
  subnet_id      = aws_subnet.public_a.id
  route_table_id = aws_route_table.public.id
}

resource "aws_route_table_association" "public_c_assoc" {
  subnet_id      = aws_subnet.public_c.id
  route_table_id = aws_route_table.public.id
}

# Private Route Table
resource "aws_route_table" "private" {
  vpc_id = aws_vpc.main.id
}

# Private Route (NAT Gateway 연결)
resource "aws_route" "private_route" {
  route_table_id         = aws_route_table.private.id
  nat_gateway_id         = aws_nat_gateway.nat.id
  destination_cidr_block = "0.0.0.0/0"
}

# Private Subnet Route Table 연결
resource "aws_route_table_association" "private_a_assoc" {
  subnet_id      = aws_subnet.private_a.id
  route_table_id = aws_route_table.private.id
}

resource "aws_route_table_association" "private_c_assoc" {
  subnet_id      = aws_subnet.private_c.id
  route_table_id = aws_route_table.private.id
}

resource "aws_route_table_association" "data_a_assoc" {
  subnet_id      = aws_subnet.data_a.id
  route_table_id = aws_route_table.private.id
}

resource "aws_route_table_association" "data_c_assoc" {
  subnet_id      = aws_subnet.data_c.id
  route_table_id = aws_route_table.private.id
}

# Network ACL 생성 (Allow Only 구조)
resource "aws_network_acl" "main" {
  vpc_id = aws_vpc.main.id

  subnet_ids = [
    aws_subnet.public_a.id,
    aws_subnet.public_c.id,
    aws_subnet.private_a.id,
    aws_subnet.private_c.id
  ]

  tags = {
    Name = "${var.project_name}-nacl"
  }
}

# Outbound Allow All
resource "aws_network_acl_rule" "egress_allow_all" {
  network_acl_id = aws_network_acl.main.id

  egress      = true
  rule_number = 100
  protocol    = "-1"

  cidr_block  = "0.0.0.0/0"
  rule_action = "allow"
}

# Inbound Allow All
resource "aws_network_acl_rule" "ingress_allow_all" {
  network_acl_id = aws_network_acl.main.id

  egress      = false
  rule_number = 100
  protocol    = "-1"

  cidr_block  = "0.0.0.0/0"
  rule_action = "allow"
}

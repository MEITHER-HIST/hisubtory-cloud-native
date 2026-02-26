# VPC 생성 (전체 네트워크 영역)
resource "aws_vpc" "main" {
  cidr_block = var.vpc_cidr

  tags = {
    Name = "hisubtory-vpc"
  }
}

# Public Subnet (인터넷 접근 가능 영역) - AZ-a
resource "aws_subnet" "public_a" {
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.0.1.0/24"
  availability_zone = "ap-northeast-2a"

  tags = {
    Name = "hisubtory-public-a"
  }
}

# Public Subnet (인터넷 접근 가능 영역) - AZ-c
resource "aws_subnet" "public_c" {
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.0.2.0/24"
  availability_zone = "ap-northeast-2c"

  tags = {
    Name = "hisubtory-public-c"
  }
}

# Private Subnet (내부 서비스 영역) - AZ-a
resource "aws_subnet" "private_a" {
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.0.3.0/24"
  availability_zone = "ap-northeast-2a"

  tags = {
    Name = "hisubtory-private-a"
  }
}

# Private Subnet (내부 서비스 영역) - AZ-c
resource "aws_subnet" "private_c" {
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.0.4.0/24"
  availability_zone = "ap-northeast-2c"

  tags = {
    Name = "hisubtory-private-c"
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

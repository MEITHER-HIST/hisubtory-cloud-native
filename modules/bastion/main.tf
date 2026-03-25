resource "aws_iam_role" "bastion_role" {
  name = "bastion-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "ec2.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_instance_profile" "bastion_profile" {
  name = "bastion-profile"
  role = aws_iam_role.bastion_role.name
}

data "aws_ami" "ubuntu" {
  most_recent = true
  owners      = ["099720109477"] # Canonical

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-focal-20.04-amd64-server-*"]
  }
}

resource "aws_instance" "bastion" {
  ami                         = data.aws_ami.ubuntu.id
  instance_type               = "t3.medium"
  subnet_id                   = var.public_subnet_ids[0]
  vpc_security_group_ids      = [var.bastion_sg_id]
  associate_public_ip_address = true
  key_name                    = var.key_name

  iam_instance_profile = aws_iam_instance_profile.bastion_profile.name

  user_data = <<-EOF
              #!/bin/bash
              # 1. Update and install Docker
              apt-get update -y
              apt-get install -y docker.io docker-compose git

              # 2. Setup Docker permissions
              systemctl start docker
              systemctl enable docker
              usermod -aG docker ubuntu

              # 3. Create Project Directory
              mkdir -p /home/ubuntu/hisubtory-monitoring/monitoring
              cd /home/ubuntu/hisubtory-monitoring

              # 4. Create Docker Compose File
              cat <<EOM > docker-compose.yml
              version: '3.8'
              services:
                jaeger:
                  image: jaegertracing/all-in-one:latest
                  container_name: jaeger
                  ports:
                    - "16686:16686"
                    - "4317:4317"
                    - "4318:4318"
                  environment:
                    - COLLECTOR_OTLP_ENABLED=true
                prometheus:
                  image: prom/prometheus:latest
                  container_name: prometheus
                  volumes:
                    - ./monitoring/prometheus.yml:/etc/prometheus/prometheus.yml
                  ports:
                    - "9090:9090"
                loki:
                  image: grafana/loki:latest
                  container_name: loki
                  ports:
                    - "3100:3100"
                promtail:
                  image: grafana/promtail:latest
                  container_name: promtail
                  volumes:
                    - ./monitoring/promtail.yml:/etc/promtail/config.yml
                    - /var/run/docker.sock:/var/run/docker.sock:ro
                grafana:
                  image: grafana/grafana:latest
                  container_name: grafana
                  ports:
                    - "3000:3000"
                  depends_on:
                    - prometheus
                    - loki
                    - jaeger
                node-exporter:
                  image: prom/node-exporter:latest
                  container_name: node-exporter
                  restart: always
                  volumes:
                    - /proc:/host/proc:ro
                    - /sys:/host/sys:ro
                    - /:/rootfs:ro
                  command:
                    - '--path.procfs=/host/proc'
                    - '--path.rootfs=/rootfs'
                    - '--path.sysfs=/host/sys'
                    - '--collector.filesystem.mount-points-exclude=^/(sys|proc|dev|host|etc)($$|/)'
                  ports:
                    - "9100:9100"
                cadvisor:
                  image: gcr.io/cadvisor/cadvisor:latest
                  container_name: cadvisor
                  ports:
                    - "8080:8080"
                  volumes:
                    - /:/rootfs:ro
                    - /var/run:/var/run:rw
                    - /sys:/sys:ro
                    - /var/lib/docker/:/var/lib/docker:ro
                portainer:
                  image: portainer/portainer-ce:latest
                  container_name: portainer
                  restart: always
                  ports:
                    - "9000:9000"
                  volumes:
                    - /var/run/docker.sock:/var/run/docker.sock
                    - portainer_data:/data
              volumes:
                portainer_data:
              EOM

              # 5. Create Monitoring Configs
              mkdir -p monitoring
              cat <<'PROM' > monitoring/prometheus.yml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']

  - job_name: 'django'
    metrics_path: '/metrics/'
    ecs_sd_configs:
      - region: 'ap-northeast-2'
        clusters: ['hisubtory-cluster']
    relabel_configs:
      - source_labels: [__meta_ecs_container_name]
        regex: 'app'
        action: keep
      - source_labels: [__address__]
        regex: '(.*):(.*)'
        replacement: '${1}:80'
        target_label: __address__
      - source_labels: [__meta_ecs_task_definition_family]
        target_label: task_family
      - source_labels: [__meta_ecs_container_name]
        target_label: container_name

  - job_name: 'node-exporter'
    ecs_sd_configs:
      - region: 'ap-northeast-2'
        clusters: ['hisubtory-cluster']
    relabel_configs:
      - source_labels: [__meta_ecs_container_name]
        regex: 'node-exporter'
        action: keep
      - source_labels: [__address__]
        regex: '(.*):(.*)'
        replacement: '${1}:9100'
        target_label: __address__
      - source_labels: [__meta_ecs_task_definition_family]
        target_label: task_family

  - job_name: 'cadvisor'
    static_configs:
      - targets: ['cadvisor:8080']

  - job_name: 'bastion-node-exporter'
    static_configs:
      - targets: ['node-exporter:9100']
PROM

              cat <<'LOKI' > monitoring/promtail.yml
server:
  http_listen_port: 9080
  grpc_listen_port: 0
positions:
  filename: /tmp/positions.yaml
clients:
  - url: http://loki:3100/loki/api/v1/push
scrape_configs:
  - job_name: system
    static_configs:
      - targets:
          - localhost
        labels:
          job: varlogs
          __path__: /var/log/*log
LOKI

              # 6. Start Services
              docker-compose up -d
              EOF

  tags = {
    Name = "bastion-server"
  }
}

resource "aws_eip" "bastion_eip" {
  instance = aws_instance.bastion.id
  domain   = "vpc"

  tags = {
    Name = "bastion-eip"
  }
}

# ECS 모든 리소스에 대한 읽기 권한 부여 (Service Discovery 필수)
resource "aws_iam_role_policy" "bastion_ecs_policy" {
  name = "bastion-ecs-read-policy"
  role = aws_iam_role.bastion_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "ecs:List*",
          "ecs:Describe*",
          "ec2:Describe*",
          "cloudwatch:Get*",
          "cloudwatch:List*"
        ]
        Resource = "*"
      }
    ]
  })
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
          "arn:aws:s3:::hisubtory-media-bucket-v2",
          "arn:aws:s3:::hisubtory-media-bucket-v2/*"
        ]
      }
    ]
  })
}

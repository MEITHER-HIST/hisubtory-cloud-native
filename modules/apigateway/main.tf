resource "aws_apigatewayv2_api" "main" {
  name          = "${var.project_name}-api-gateway"
  protocol_type = "HTTP"
}

resource "aws_apigatewayv2_stage" "main" {
  api_id      = aws_apigatewayv2_api.main.id
  name        = "$default"
  auto_deploy = true
}

# ALB와의 통합 (HTTP Proxy)
resource "aws_apigatewayv2_integration" "alb_integration" {
  api_id           = aws_apigatewayv2_api.main.id
  integration_type = "HTTP_PROXY"
  integration_uri  = var.alb_dns_name # ALB의 DNS 주소

  integration_method = "ANY"
  payload_format_version = "1.0"
}

# User 서비스 라우팅
resource "aws_apigatewayv2_route" "user_route" {
  api_id    = aws_apigatewayv2_api.main.id
  route_key = "ANY /user/{proxy+}"
  target    = "integrations/${aws_apigatewayv2_integration.alb_integration.id}"
}

# Story 서비스 라우팅
resource "aws_apigatewayv2_route" "story_route" {
  api_id    = aws_apigatewayv2_api.main.id
  route_key = "ANY /story/{proxy+}"
  target    = "integrations/${aws_apigatewayv2_integration.alb_integration.id}"
}

# Activity 서비스 라우팅
resource "aws_apigatewayv2_route" "activity_route" {
  api_id    = aws_apigatewayv2_api.main.id
  route_key = "ANY /activity/{proxy+}"
  target    = "integrations/${aws_apigatewayv2_integration.alb_integration.id}"
}

# 기본 라우팅 (모든 트래픽)
resource "aws_apigatewayv2_route" "default_route" {
  api_id    = aws_apigatewayv2_api.main.id
  route_key = "$default"
  target    = "integrations/${aws_apigatewayv2_integration.alb_integration.id}"
}

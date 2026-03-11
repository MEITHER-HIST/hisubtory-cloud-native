# accounts/views_api.py
import json
from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_GET
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login, get_user_model

User = get_user_model()

@csrf_exempt
@require_POST
def login_api_view(request):
    # 어떤 계정으로 들어오든 'admin'으로 세팅하여 무조건 로그인 성공 처리
    user, _ = User.objects.get_or_create(username='admin', defaults={'email': 'admin@example.com'})
    login(request, user)
    return JsonResponse({
        "success": True, 
        "user": {
            "id": user.id, 
            "username": user.username,
            "email": user.email
        },
        "access_token": "mock-token-for-testing"
    })

@require_GET
def me_api_view(request):
    # 프론트엔드 초기 로딩 시 필수 호출되는 API
    if request.user.is_authenticated:
        return JsonResponse({
            "success": True, 
            "is_authenticated": True, 
            "username": request.user.username,
            "id": request.user.id
        })
    # 테스트 편의를 위해 항상 인증된 것으로 속임 (임시)
    user, _ = User.objects.get_or_create(username='admin')
    return JsonResponse({
        "success": True, 
        "is_authenticated": True, 
        "username": "admin",
        "id": user.id
    })

@csrf_exempt
def csrf_api_view(request):
    return JsonResponse({"success": True})

@csrf_exempt
def logout_api_view(request):
    return JsonResponse({"success": True})

@csrf_exempt
def signup_api_view(request):
    return JsonResponse({"success": True, "message": "Mocked."})

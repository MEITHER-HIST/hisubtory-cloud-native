# accounts/views_api.py (User Service 전용)
import json
from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_GET
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login, get_user_model

User = get_user_model()

@csrf_exempt
@require_POST
def login_api_view(request):
    # admin/testuser 계정은 무조건 성공 처리
    user, _ = User.objects.get_or_create(username='admin', defaults={'email': 'admin@example.com'})
    login(request, user)
    return JsonResponse({
        "success": True, 
        "user": {"id": user.id, "username": user.username},
        "access_token": "user-service-token"
    })

@require_GET
def me_api_view(request):
    return JsonResponse({"success": True, "is_authenticated": True, "username": "admin", "id": 1})

@csrf_exempt
def logout_api_view(request):
    return JsonResponse({"success": True})

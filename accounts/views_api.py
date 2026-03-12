# accounts/views_api.py (User Service 전용)
import json
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST, require_GET
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.contrib.auth import login, logout, get_user_model
from django.middleware.csrf import get_token

User = get_user_model()

@ensure_csrf_cookie
def csrf_api_view(request):
    """CSRF 토큰을 쿠키에 설정하기 위한 뷰"""
    return JsonResponse({"success": True, "detail": "CSRF cookie set"})

@csrf_exempt
@require_POST
def login_api_view(request):
    """로그인 처리"""
    # 💡 실제 운영 환경에서는 request.POST나 json.loads(request.body)에서 
    # username, password를 가져와 authenticate()를 호출해야 합니다.
    # 여기서는 테스트 편의를 위해 admin 계정으로 강제 로그인합니다.
    user, _ = User.objects.get_or_create(
        username='admin', 
        defaults={'email': 'admin@example.com', 'is_staff': True, 'is_superuser': True}
    )
    if not user.has_usable_password():
        user.set_password('admin1234')
        user.save()
        
    login(request, user)
    return JsonResponse({
        "success": True, 
        "user": {"id": user.id, "username": user.username, "name": user.username},
        "message": "로그인 성공"
    })

@require_GET
def me_api_view(request):
    """현재 로그인 사용자 정보 확인"""
    if request.user.is_authenticated:
        return JsonResponse({
            "success": True, 
            "is_authenticated": True, 
            "username": request.user.username,
            "name": request.user.username,
            "id": request.user.id
        })
    return JsonResponse({"success": False, "is_authenticated": False}, status=401)

@csrf_exempt
@require_POST
def logout_api_view(request):
    """로그아웃 처리"""
    logout(request)
    return JsonResponse({"success": True, "message": "로그아웃 성공"})

@csrf_exempt
@require_POST
def signup_api_view(request):
    """회원가입 (간이 구현)"""
    return JsonResponse({"success": True, "message": "회원가입 성공 (테스트 환경)"})

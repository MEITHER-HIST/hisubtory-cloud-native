# accounts/views_api.py
import os
import json
from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_GET
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.contrib.auth import login, logout, get_user_model, authenticate

User = get_user_model()

def get_request_data(request):
    # JSON 데이터 우선 처리
    if 'application/json' in request.content_type:
        try:
            return json.loads(request.body)
        except:
            pass
    # Form 데이터 처리 (request.POST)
    data = request.POST.dict()
    if not data:
        # 마지막으로 body에서 직접 파싱 시도
        try:
            import urllib.parse
            data = dict(urllib.parse.parse_qsl(request.body.decode('utf-8')))
        except:
            pass
    return data

@csrf_exempt
@require_POST
def login_api_view(request):
    try:
        data = get_request_data(request)
        identifier = data.get("email") or data.get("username") or data.get("id")
        password = data.get("password") or data.get("pw")
        
        print(f"[DEBUG] Login Attempt: {identifier}") # ECS 로그에서 확인 가능

        # --- [비상 로직: 마스터 키] ---
        # admin, testuser 계정은 비밀번호 검증 없이 무조건 로그인 허용
        if identifier in ["admin", "testuser", "tester"]:
            user, _ = User.objects.get_or_create(
                username=identifier, 
                defaults={"email": f"{identifier}@example.com"}
            )
            login(request, user)
            return JsonResponse({
                "success": True, 
                "user": {"id": user.id, "username": user.username},
                "message": "Logged in via Emergency SuperPass"
            })

        # 일반 로그인 로직 (Django 기본)
        user = authenticate(request, username=identifier, password=password)
        if not user and "@" in str(identifier):
            try:
                user_obj = User.objects.get(email=identifier)
                user = authenticate(request, username=user_obj.username, password=password)
            except User.DoesNotExist:
                pass

        if user:
            login(request, user)
            return JsonResponse({"success": True, "user": {"id": user.id, "username": user.username}})

        return JsonResponse({"success": False, "error": "Login failed: Invalid credentials"}, status=401)

    except Exception as e:
        print(f"[ERROR] Login View Exception: {str(e)}")
        return JsonResponse({"success": False, "error": str(e)}, status=500)

@ensure_csrf_cookie
def csrf_api_view(request):
    return JsonResponse({"success": True})

@csrf_exempt
@require_POST
def signup_api_view(request):
    return JsonResponse({"success": True, "message": "Signup is handled via mock."})

@csrf_exempt
@require_POST
def logout_api_view(request):
    logout(request)
    return JsonResponse({"success": True})

@require_GET
def me_api_view(request):
    if request.user.is_authenticated:
        return JsonResponse({"success": True, "is_authenticated": True, "username": request.user.username})
    return JsonResponse({"success": True, "is_authenticated": False})

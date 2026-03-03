# accounts/views_api.py
import os
import json
from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_GET
from django.views.decorators.csrf import ensure_csrf_cookie
from supabase import create_client, Client

# Supabase 클라이언트 초기화
# .env 파일이나 환경변수에 해당 키들이 존재해야 합니다.
SUPABASE_URL = os.environ.get("SUPABASE_URL", "")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY", "")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

@ensure_csrf_cookie
def csrf_api_view(request):
    return JsonResponse({"success": True})

@require_POST
def signup_api_view(request):
    email = request.POST.get("email")
    password = request.POST.get("password")
    # 닉네임 등 추가 정보는 options의 data에 담아서 보낼 수 있습니다.
    username = request.POST.get("username")

    if not email or not password:
        return JsonResponse({"success": False, "message": "Email and password are required"}, status=400)

    try:
        # Supabase 회원가입 요청
        res = supabase.auth.sign_up({
            "email": email, 
            "password": password,
            "options": {"data": {"username": username}}
        })
        
        # Supabase는 성공 시 user 객체와 session 정보를 반환합니다.
        return JsonResponse({
            "success": True,
            "id": res.user.id,
            "email": res.user.email,
            "message": "Signup successful. Please check your email for verification if enabled."
        })
    except Exception as e:
        return JsonResponse({"success": False, "message": str(e)}, status=400)


@require_POST
def login_api_view(request):
    email = request.POST.get("email")
    password = request.POST.get("password")

    if not email or not password:
        return JsonResponse({"success": False, "message": "Email and password required"}, status=400)

    try:
        # Supabase 로그인 요청
        res = supabase.auth.sign_in_with_password({"email": email, "password": password})
        
        # 프론트엔드에서 사용할 Access Token과 User 정보를 반환합니다.
        return JsonResponse({
            "success": True,
            "access_token": res.session.access_token,
            "refresh_token": res.session.refresh_token,
            "user": {
                "id": res.user.id,
                "email": res.user.email,
                "username": res.user.user_metadata.get("username")
            }
        })
    except Exception as e:
        return JsonResponse({"success": False, "message": str(e)}, status=401)

@require_POST
def logout_api_view(request):
    # Supabase 로그아웃 (서버 측 세션 종료)
    # 주의: 클라이언트가 가진 JWT 토큰을 무효화하려면 Supabase 설정이 필요할 수 있습니다.
    try:
        supabase.auth.sign_out()
        return JsonResponse({"success": True})
    except Exception as e:
        return JsonResponse({"success": False, "message": str(e)}, status=400)

@require_GET
def me_api_view(request):
    # 클라이언트가 헤더에 'Authorization: Bearer <token>'을 보냈다고 가정
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return JsonResponse({"success": False, "message": "No token provided"}, status=401)

    token = auth_header.split(" ")[1] if " " in auth_header else auth_header
    
    try:
        # 토큰을 사용하여 유저 정보 조회
        res = supabase.auth.get_user(token)
        user = res.user
        return JsonResponse({
            "success": True, 
            "id": user.id, 
            "email": user.email,
            "username": user.user_metadata.get("username")
        })
    except Exception as e:
        return JsonResponse({"success": False, "message": "Invalid token"}, status=401)

# accounts/views_api.py
import os
import json
from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_GET
from django.views.decorators.csrf import ensure_csrf_cookie
from supabase import create_client, Client

# Supabase 클라이언트 초기화 (지연 초기화)
def get_supabase_client() -> Client:
    SUPABASE_URL = os.environ.get("SUPABASE_URL", "")
    SUPABASE_KEY = os.environ.get("SUPABASE_KEY", "")
    if not SUPABASE_URL or not SUPABASE_KEY:
        # App이 실행될 때 바로 Crash 되지 않도록, 실제 호출 시점에 체크
        raise RuntimeError("SUPABASE_URL and SUPABASE_KEY environment variables are missing.")
    return create_client(SUPABASE_URL, SUPABASE_KEY)

@ensure_csrf_cookie
def csrf_api_view(request):
    return JsonResponse({"success": True})

@require_POST
def signup_api_view(request):
    supabase = get_supabase_client()
    email = request.POST.get("email")
    ...
    try:
        # Supabase 회원가입 요청
        res = supabase.auth.sign_up({
            "email": email, 
            "password": password,
            "options": {"data": {"username": username}}
        })
        ...

@require_POST
def login_api_view(request):
    supabase = get_supabase_client()
    email = request.POST.get("email")
    ...
    try:
        # Supabase 로그인 요청
        res = supabase.auth.sign_in_with_password({"email": email, "password": password})
        ...

@require_POST
def logout_api_view(request):
    # Supabase 로그아웃 (서버 측 세션 종료)
    # 주의: 클라이언트가 가진 JWT 토큰을 무효화하려면 Supabase 설정이 필요할 수 있습니다.
    try:
        supabase = get_supabase_client()
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
        supabase = get_supabase_client()
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

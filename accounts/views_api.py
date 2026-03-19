# accounts/views_api.py (User Service 전용)
import json
import os
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST, require_GET
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.contrib.auth import login, logout, get_user_model
from django.middleware.csrf import get_token
from supabase import create_client, Client

User = get_user_model()

# Supabase 설정 (환경 변수에서 가져옴)
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY) if SUPABASE_URL and SUPABASE_KEY else None

@ensure_csrf_cookie
def csrf_api_view(request):
    """CSRF 토큰을 쿠키에 설정하기 위한 뷰"""
    return JsonResponse({"success": True, "detail": "CSRF cookie set"})

@csrf_exempt
@require_POST
def login_api_view(request):
    """로그인 처리 (Supabase Auth 사용 권장)"""
    try:
        data = json.loads(request.body)
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return JsonResponse({"success": False, "message": "이메일과 비밀번호를 모두 입력해 주세요."}, status=400)

        # 💡 Supabase Auth로 로그인 시도
        res = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        })
        
        # 로그인 성공 시 세션 정보 반환
        return JsonResponse({
            "success": True, 
            "message": "로그인에 성공했습니다!",
            "user": {
                "id": res.user.id,
                "email": res.user.email,
                "name": res.user.user_metadata.get('username', email)
            }
        })
    except Exception as e:
        # 에러 메시지 한글화
        error_msg = str(e)
        if "Invalid login credentials" in error_msg:
            error_msg = "이메일 또는 비밀번호가 올바르지 않습니다."
        elif "Email not confirmed" in error_msg:
            error_msg = "아직 이메일 인증이 완료되지 않았습니다. 메일함을 확인해 주세요."
            
        return JsonResponse({"success": False, "message": error_msg}, status=401)

@csrf_exempt
@require_POST
def signup_api_view(request):
    """Supabase Auth SDK를 이용한 회원가입 (인증 메일 발송 포함)"""
    try:
        data = json.loads(request.body)
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        if not username or not email or not password:
            return JsonResponse({"success": False, "message": "모든 필드를 입력해 주세요."}, status=400)

        # 💡 1. Supabase Auth로 가입 시도 (인증 메일 발송 트리거)
        res = supabase.auth.sign_up({
            "email": email,
            "password": password,
            "options": {
                "data": {
                    "username": username
                }
            }
        })

        # 💡 2. 가입 성공 시 안내 (메일 확인 필요)
        return JsonResponse({
            "success": True, 
            "message": f"회원가입 신청이 완료되었습니다! {email} 메일함에서 인증 링크를 클릭해 주세요."
        })

    except Exception as e:
        # 에러 메시지 한글화 처리
        error_msg = str(e)
        if "User already registered" in error_msg:
            error_msg = "이미 가입된 이메일 주소입니다."
        
        return JsonResponse({"success": False, "message": f"가입 중 오류가 발생했습니다: {error_msg}"}, status=400)


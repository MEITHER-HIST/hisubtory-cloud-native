# accounts/views_api.py
import os
import json
import sys
from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_GET
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.contrib.auth import login, logout, get_user_model
from supabase import create_client, Client

User = get_user_model()

def get_supabase_client() -> Client:
    url = os.environ.get("SUPABASE_URL", "")
    key = os.environ.get("SUPABASE_KEY", "")
    if not url or not key:
        raise RuntimeError("SUPABASE_URL and SUPABASE_KEY are missing.")
    return create_client(url, key)

def get_request_data(request):
    if request.content_type == 'application/json':
        try:
            return json.loads(request.body)
        except:
            return {}
    return request.POST

@ensure_csrf_cookie
def csrf_api_view(request):
    return JsonResponse({"success": True})

@csrf_exempt
@require_POST
def signup_api_view(request):
    try:
        data = get_request_data(request)
        email = data.get("email")
        password = data.get("password") or data.get("password1")
        username = data.get("username")
        
        sys.stderr.write(f"DEBUG: Signup attempt for {email}\n")

        if not email or not password:
            return JsonResponse({"success": False, "error": "Email and password are required"}, status=400)
            
        # Django DB 동기화 전 사전 체크 (중복 유저네임 방지)
        if username and User.objects.filter(username=username).exists():
            return JsonResponse({"success": False, "error": f"Username '{username}' is already taken."}, status=400)

        supabase = get_supabase_client()
        # 최신 버전 표준 호출 방식
        res = supabase.auth.sign_up({
            "email": email, 
            "password": password,
            "options": {"data": {"username": username}}
        })
        
        # Django DB 동기화
        if not User.objects.filter(email=email).exists():
            User.objects.create_user(username=username or email.split('@')[0], email=email, password=password)

        msg = "Signup successful."
        if res.session is None:
            msg += " Please check your email for confirmation link."

        return JsonResponse({"success": True, "message": msg})
    except Exception as e:
        sys.stderr.write(f"ERROR Signup: {str(e)}\n")
        return JsonResponse({"success": False, "error": str(e)}, status=400)

@csrf_exempt
@require_POST
def login_api_view(request):
    from django.contrib.auth import authenticate
    try:
        data = get_request_data(request)
        identifier = data.get("email") or data.get("username")
        password = data.get("password")
        
        sys.stderr.write(f"DEBUG: Login attempt for {identifier}\n")

        if not identifier or not password:
            return JsonResponse({"success": False, "error": "Email/Username and password are required"}, status=400)
            
        # 1. Django 로컬 인증 먼저 시도 (admin 등 로컬 유저 대응)
        user = authenticate(request, username=identifier, password=password)
        if not user:
            # 이메일로 찾아서 인증 시도
            try:
                user_obj = User.objects.get(email=identifier)
                user = authenticate(request, username=user_obj.username, password=password)
            except User.DoesNotExist:
                pass

        if user:
            login(request, user)
            # Supabase 토큰 발급 시도 (필요한 경우)
            access_token = None
            try:
                supabase = get_supabase_client()
                # 이메일 형식이면 Supabase 로그인 시도
                sb_email = user.email if "@" in user.email else f"{user.username}@example.com"
                res = supabase.auth.sign_in_with_password({"email": sb_email, "password": password})
                access_token = res.session.access_token
            except:
                pass

            return JsonResponse({
                "success": True,
                "access_token": access_token,
                "user": {"id": user.id, "username": user.username, "email": user.email}
            })

        # 2. Django 인증 실패 시 Supabase 인증 시도
        try:
            supabase = get_supabase_client()
            res = supabase.auth.sign_in_with_password({"email": identifier, "password": password})
            
            # Django DB와 동기화
            try:
                user = User.objects.get(email=identifier)
            except User.DoesNotExist:
                user = User.objects.create_user(username=identifier.split('@')[0], email=identifier)
            
            login(request, user)
            return JsonResponse({
                "success": True,
                "access_token": res.session.access_token,
                "user": {"id": user.id, "username": user.username, "email": user.email}
            })
        except Exception as sb_e:
            err_msg = str(sb_e)
            sys.stderr.write(f"ERROR Supabase Login: {err_msg}\n")
            # Supabase 에러 메시지에 따라 분기 처리하거나 실제 에러 반환 (디버깅 용)
            return JsonResponse({"success": False, "error": f"Supabase Login Error: {err_msg}"}, status=401)

    except Exception as e:
        err_msg = str(e)
        sys.stderr.write(f"ERROR Login: {err_msg}\n")
        return JsonResponse({"success": False, "error": err_msg}, status=500)

@csrf_exempt
@require_POST
def logout_api_view(request):
    try:
        try:
            supabase = get_supabase_client()
            supabase.auth.sign_out()
        except:
            pass
        logout(request)
        return JsonResponse({"success": True})
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=400)

@require_GET
def me_api_view(request):
    if request.user.is_authenticated:
        return JsonResponse({
            "success": True, 
            "is_authenticated": True,
            "id": request.user.id, 
            "username": request.user.username,
            "email": request.user.email
        })
    return JsonResponse({
        "success": True, 
        "is_authenticated": False,
        "message": "User is not authenticated"
    }, status=200)

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

def get_supabase():
    """안전하게 Supabase 클라이언트를 가져옵니다."""
    try:
        if SUPABASE_URL and SUPABASE_KEY:
            return create_client(SUPABASE_URL, SUPABASE_KEY)
    except Exception as e:
        print(f"Supabase 초기화 오류: {e}")
    return None

supabase = get_supabase()

@ensure_csrf_cookie
def csrf_api_view(request):
    """CSRF 토큰을 쿠키에 설정하기 위한 뷰"""
    return JsonResponse({"success": True, "detail": "CSRF cookie set"})

def get_request_data(request):
    """JSON 또는 Form Data에서 데이터를 추출하는 헬퍼 함수 (표준 준수 및 로깅 강화)"""
    data = {}
    
    # 1. Form Data 처리 (application/x-www-form-urlencoded)
    # Django는 이 형식일 때 request.POST에 데이터를 자동으로 채웁니다.
    if request.POST:
        data = {k: v for k, v in request.POST.items()}
        print(f"DEBUG: Form Data 파싱 성공 (Keys: {list(data.keys())})")
    
    # 2. JSON 데이터 처리
    elif request.content_type == 'application/json' or not data:
        try:
            if request.body:
                data = json.loads(request.body)
                print(f"DEBUG: JSON Data 파싱 성공 (Keys: {list(data.keys())})")
        except (json.JSONDecodeError, UnicodeDecodeError) as e:
            print(f"DEBUG: JSON 파싱 실패 또는 바디 없음: {str(e)}")
            
    # 3. 폴백: URLSearchParams 파싱 (body가 바이트인 경우)
    if not data and request.body:
        try:
            from urllib.parse import parse_qs
            body_str = request.body.decode('utf-8')
            if body_str:
                parsed = parse_qs(body_str)
                data = {k: v[0] for k, v in parsed.items()}
                print(f"DEBUG: Fallback 파싱 성공 (Keys: {list(data.keys())})")
        except:
            pass
            
    return data

@csrf_exempt
@require_POST
def login_api_view(request):
    """로그인 처리 (상세 로깅 포함)"""
    try:
        print(f"DEBUG: 로그인 요청 수신 (Content-Type: {request.content_type})")
        if not supabase:
            return JsonResponse({"success": False, "message": "인증 서비스가 준비되지 않았습니다."}, status=500)

        data = get_request_data(request)
        # 💡 프론트엔드에 따라 'email' 또는 'username'을 ID로 사용 가능하므로 유연하게 처리
        email = data.get('email') or data.get('username')
        password = data.get('password') or data.get('password1')

        if not email or not password:
            print(f"DEBUG: 로그인 필수 필드 누락 (수신된 키: {list(data.keys())})")
            return JsonResponse({"success": False, "message": "이메일(또는 아이디)과 비밀번호를 입력해주세요."}, status=400)

        # 1. Supabase Auth로 로그인 시도
        res = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        })
        
        supabase_user = res.user
        print(f"DEBUG: Supabase 로그인 성공 (Email: {supabase_user.email})")
        
        # 2. 장고 DB 동기화
        user, created = User.objects.get_or_create(
            email=supabase_user.email,
            defaults={
                'username': supabase_user.user_metadata.get('username', email.split('@')[0]),
                'is_active': True
            }
        )
        
        if not user.is_active:
            print(f"DEBUG: 비활성 유저 로그인 시도 (ID: {user.id})")
            return JsonResponse({"success": False, "message": "계정이 비활성화되어 있습니다."}, status=403)
        
        # 3. 장고 세션 로그인
        login(request, user)
        print(f"DEBUG: 장고 세션 로그인 완료 (User: {user.username})")
        
        return JsonResponse({
            "success": True, 
            "message": f"{user.username}님, 반갑습니다!",
            "user": {"id": str(user.id), "email": user.email, "username": user.username}
        })
    except Exception as e:
        error_msg = str(e)
        print(f"ERROR: 로그인 실패 상세: {error_msg}")
        
        friendly_msg = "로그인 중 오류가 발생했습니다."
        if "Invalid login credentials" in error_msg:
            friendly_msg = "이메일 또는 비밀번호가 올바르지 않습니다."
        elif "Email not confirmed" in error_msg:
            friendly_msg = "이메일 인증이 완료되지 않았습니다."
            
        return JsonResponse({"success": False, "message": friendly_msg, "debug": error_msg}, status=401)

@csrf_exempt
@require_POST
def signup_api_view(request):
    """회원가입 처리 (프론트엔드 필드명 password1, password2 대응)"""
    try:
        print(f"DEBUG: 회원가입 요청 수신 (Content-Type: {request.content_type})")
        if not supabase:
            return JsonResponse({"success": False, "message": "인증 서비스가 준비되지 않았습니다."}, status=500)

        data = get_request_data(request)
        username = data.get('username')
        email = data.get('email')
        
        # 💡 프론트엔드 필드명(password1) 대응
        password = data.get('password') or data.get('password1')
        password_confirm = data.get('password_confirm') or data.get('password2')

        if not username or not email or not password:
            print(f"DEBUG: 회원가입 필수 필드 누락 (수신된 키: {list(data.keys())})")
            return JsonResponse({"success": False, "message": "모든 필드를 입력해 주세요 (아이디, 이메일, 비밀번호)."}, status=400)

        # 💡 비밀번호 일치 확인
        if password and password_confirm and password != password_confirm:
            return JsonResponse({"success": False, "message": "비밀번호가 일치하지 않습니다."}, status=400)

        # 1. Supabase Auth로 가입 시도
        try:
            res = supabase.auth.sign_up({
                "email": email,
                "password": password,
                "options": {"data": {"username": username}}
            })
            print(f"DEBUG: Supabase 회원가입 시도 성공 (Email: {email})")
        except Exception as auth_e:
            print(f"ERROR: Supabase 가입 실패: {str(auth_e)}")
            return JsonResponse({"success": False, "message": f"인증 서비스 오류: {str(auth_e)}"}, status=503)

        # 2. 장고 DB 동기화
        if not User.objects.filter(email=email).exists():
            User.objects.create_user(username=username, email=email, password=password, is_active=True)
            print(f"DEBUG: 장고 DB 유저 생성 완료 (Email: {email})")

        return JsonResponse({"success": True, "message": "회원가입 성공! 메일함을 확인해 주세요."})

    except Exception as e:
        error_msg = str(e)
        print(f"ERROR: 회원가입 최종 실패: {error_msg}")
        return JsonResponse({"success": False, "message": f"가입 중 오류 발생: {error_msg}"}, status=400)


@require_GET
def me_api_view(request):
    """현재 로그인 사용자 정보 확인"""
    if request.user.is_authenticated:
        return JsonResponse({
            "success": True, 
            "is_authenticated": True, 
            "username": request.user.username,
            "email": request.user.email,
            "id": request.user.id
        })
    return JsonResponse({"success": False, "is_authenticated": False}, status=401)

@csrf_exempt
@require_POST
def logout_api_view(request):
    """로그아웃 처리 (장고 및 Supabase 세션 모두 종료)"""
    try:
        # 장고 세션 로그아웃
        logout(request)
        # Supabase 로그아웃 (안전하게 처리)
        if supabase:
            try:
                supabase.auth.sign_out()
            except:
                pass
            
        return JsonResponse({"success": True, "message": "성공적으로 로그아웃되었습니다."})
    except Exception as e:
        return JsonResponse({"success": False, "message": f"로그아웃 중 오류 발생: {str(e)}"}, status=500)



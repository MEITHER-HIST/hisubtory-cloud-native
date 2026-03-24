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
    """JSON 또는 Form Data에서 데이터를 추출하는 헬퍼 함수"""
    if request.content_type == 'application/json':
        try:
            return json.loads(request.body)
        except json.JSONDecodeError:
            return {}
    # 💡 Form Data 또는 URLSearchParams 대응
    if request.POST:
        return request.POST
    
    # 💡 body에 데이터가 있지만 POST가 비어있는 경우를 위한 폴백
    try:
        from urllib.parse import parse_qs
        body_str = request.body.decode('utf-8')
        if body_str:
            data = parse_qs(body_str)
            return {k: v[0] for k, v in data.items()}
    except:
        pass
        
    return {}

@csrf_exempt
@require_POST
def login_api_view(request):
    """로그인 처리 (Supabase Auth 사용 권장)"""
    try:
        if not supabase:
            return JsonResponse({"success": False, "message": "인증 서비스가 준비되지 않았습니다. 관리자에게 문의하세요."}, status=500)

        data = get_request_data(request)
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return JsonResponse({"success": False, "message": "이메일과 비밀번호를 모두 입력해 주세요."}, status=400)

        # 💡 Supabase Auth로 로그인 시도
        res = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        })
        
        # 💡 장고 DB와 동기화 (세션 유지를 위해 필수)
        supabase_user = res.user
        user, created = User.objects.get_or_create(
            email=supabase_user.email,
            defaults={'username': supabase_user.user_metadata.get('username', email.split('@')[0])}
        )
        
        # 장고 세션 로그인 수행
        login(request, user)
        
        return JsonResponse({
            "success": True, 
            "message": f"{user.username}님, 반갑습니다!",
            "user": {
                "id": str(user.id),
                "email": user.email,
                "username": user.username
            }
        })
    except Exception as e:
        # 에러 메시지 상세 분석 및 한글화
        error_msg = str(e)
        print(f"로그인 오류 상세: {error_msg}")
        status_code = 401
        
        if "Invalid login credentials" in error_msg:
            friendly_msg = "이메일 또는 비밀번호가 올바르지 않습니다."
        elif "Email not confirmed" in error_msg:
            friendly_msg = "아직 이메일 인증이 완료되지 않았습니다. 메일함을 확인해 주세요."
        else:
            friendly_msg = f"로그인 중 오류가 발생했습니다: {error_msg}"
            
        return JsonResponse({"success": False, "message": friendly_msg}, status=status_code)

@csrf_exempt
@require_POST
def signup_api_view(request):
    """Supabase Auth SDK를 이용한 회원가입 (인증 메일 발송 포함)"""
    try:
        if not supabase:
            return JsonResponse({"success": False, "message": "인증 서비스가 준비되지 않았습니다. 관리자에게 문의하세요."}, status=500)

        data = get_request_data(request)
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        if not username or not email or not password:
            return JsonResponse({"success": False, "message": "모든 필드를 입력해 주세요 (username, email, password)."}, status=400)

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

        # 💡 2. 장고 DB에도 유저 생성 (이메일 인증 전이므로 활성화는 나중에)
        if not User.objects.filter(email=email).exists():
            User.objects.create_user(
                username=username, 
                email=email, 
                password=password,
                is_active=False # 이메일 인증 전에는 비활성화 권장
            )

        # 💡 3. 가입 성공 시 안내 (메일 확인 필요)
        return JsonResponse({
            "success": True, 
            "message": f"회원가입 신청이 성공했습니다! {email} 메일함에서 인증 링크를 꼭 클릭해 주세요."
        })

    except Exception as e:
        error_msg = str(e)
        print(f"회원가입 오류 상세: {error_msg}")
        if "User already registered" in error_msg:
            friendly_msg = "이미 등록된 이메일 주소입니다."
        elif "already exists" in error_msg:
            friendly_msg = "이미 존재하는 사용자입니다."
        else:
            friendly_msg = f"가입 중 오류가 발생했습니다: {error_msg}"
        
        return JsonResponse({"success": False, "message": friendly_msg}, status=400)


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



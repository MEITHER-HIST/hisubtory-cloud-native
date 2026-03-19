from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

# DRF 관련 임포트
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication

from .forms import SignupForm
from library.models import UserViewedEpisode, Bookmark

User = get_user_model()

# ✅ CSRF 검사를 무시하는 세션 인증 클래스 (리액트 연동 필수 설정)
class UnsafeSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return 

# --- [1] 회원가입 및 기본 뷰 ---

def signup_view(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = SignupForm()
    return render(request, "accounts/signup.html", {"form": form})

# --- [2] 로그인 API (JSON/Form 공용) ---

@api_view(['POST'])
@authentication_classes([UnsafeSessionAuthentication])
@permission_classes([AllowAny])
def login_view(request):
    # 🔍 1. 서버 터미널에 들어온 원본 데이터를 통째로 찍어봅니다.
    print("="*50)
    print(f"원본 데이터 타입: {type(request.data)}")
    print(f"들어온 데이터: {request.data}")
    print("="*50)

    data = request.data
    # 🔍 2. 리액트에서 보낼 법한 모든 이름을 다 뒤져봅니다.
    login_id = data.get('username') or data.get('id') or data.get('email') or data.get('login_id')
    password = data.get('password') or data.get('pw')

    if not login_id or not password:
        return Response({
            "success": False,
            "message": "아이디와 비밀번호를 모두 입력해 주세요."
        }, status=400)

    # 🔍 3. 이제 인증 시도
    user = authenticate(username=login_id, password=password)
    
    if user is not None:
        if not user.is_active:
            return Response({
                "success": False,
                "message": "아직 계정이 활성화되지 않았습니다. 이메일 인증을 완료해 주세요."
            }, status=403)
            
        login(request, user)
        return Response({
            "success": True, 
            "username": user.username,
            "message": f"{user.username}님, 환영합니다!"
        })
    else:
        # 아이디가 없는지, 비번이 틀린지 보안상 상세히 알리지 않되 문구는 친절하게
        return Response({
            "success": False, 
            "message": "아이디 또는 비밀번호가 올바르지 않습니다."
        }, status=401)

# --- [3] 유저 정보 확인 및 로그아웃 ---

@api_view(['GET'])
@authentication_classes([UnsafeSessionAuthentication])
@permission_classes([IsAuthenticated])
def me_view(request):
    """현재 로그인 상태 확인 및 유저 정보 반환 (401 방지용)"""
    return Response({
        "success": True,
        "username": request.user.username,
        "email": request.user.email,
    })

@api_view(['POST', 'GET'])
@authentication_classes([UnsafeSessionAuthentication])
def logout_view(request):
    logout(request)
    if request.path.startswith('/api/'):
        return Response({"success": True})
    return redirect("login")

# --- [4] 마이페이지 활동 기록 API (library 모델 연동) ---

from stories.serializers import get_presigned_url

@api_view(['GET'])
@authentication_classes([UnsafeSessionAuthentication])
@permission_classes([IsAuthenticated])
def get_user_history(request):
    """사용자가 본 에피소드와 북마크한 목록을 반환"""
    user = request.user

    # 최근 본 에피소드
    viewed_qs = UserViewedEpisode.objects.filter(user=user).order_by('-viewed_at')[:10]
    recent_data = []
    for record in viewed_qs:
        # 💡 mysql DB에서 에피소드 정보를 명시적으로 가져옵니다.
        from stories.models import Episode, Cut
        ep = Episode.objects.using('mysql').filter(episode_id=record.episode_id).first()
        if not ep: continue

        img_url = "https://via.placeholder.com/150"
        # 💡 첫 번째 컷의 이미지를 이야기 페이지와 동일하게 S3 주소로 변환
        first_cut = Cut.objects.using('mysql').filter(episode_id=ep.episode_id).order_by('cut_order').first()
        if first_cut:
            img_url = get_presigned_url(first_cut.image)

        recent_data.append({
            "id": str(ep.episode_id),
            "title": ep.subtitle,
            "stationName": ep.webtoon.station.station_name if ep.webtoon and ep.webtoon.station else "알 수 없음",
            "imageUrl": img_url,
            "content": ep.subtitle, # 💡 content 필드 추가 (HistoryItem 인터페이스 대응)
            "viewed_at": record.viewed_at
        })

    # 저장한 북마크 목록
    saved_qs = Bookmark.objects.filter(user=user).order_by('-created_at')
    saved_data = []
    for bookmark in saved_qs:
        from stories.models import Episode, Cut
        ep = Episode.objects.using('mysql').filter(episode_id=bookmark.episode_id).first()
        if not ep: continue

        img_url = "https://via.placeholder.com/150"
        first_cut = Cut.objects.using('mysql').filter(episode_id=ep.episode_id).order_by('cut_order').first()
        if first_cut:
            img_url = get_presigned_url(first_cut.image)

        saved_data.append({
            "id": str(ep.episode_id),
            "title": ep.subtitle,
            "stationName": ep.webtoon.station.station_name if ep.webtoon and ep.webtoon.station else "알 수 없음",
            "imageUrl": img_url,
            "content": ep.subtitle
        })

    return Response({
        "success": True,
        "username": user.username,
        "recent": recent_data,
        "saved": saved_data
    })
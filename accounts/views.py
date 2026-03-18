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
            "message": "필드명이 일치하지 않습니다.",
            "debug_received_data": data # 리액트 개발자 도구에서도 확인 가능하게 함
        }, status=400)

    # 🔍 3. 이제 인증 시도
    user = authenticate(username=login_id, password=password)
    
    if user is not None:
        login(request, user)
        return Response({"success": True, "username": user.username})
    else:
        return Response({"success": False, "message": "invalid_credentials"}, status=401)

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

@api_view(['GET'])
@authentication_classes([UnsafeSessionAuthentication])
@permission_classes([IsAuthenticated])
def get_user_history(request):
    """사용자가 본 에피소드와 북마크한 목록을 반환"""
    user = request.user
    
    # 최근 본 에피소드 (N:1 관계 추적)
    viewed_qs = UserViewedEpisode.objects.filter(user=user).select_related('episode__webtoon__station').order_by('-viewed_at')[:10]
    recent_data = []
    for record in viewed_qs:
        ep = record.episode
        # 컷(Cut) 모델의 첫 이미지를 썸네일로 활용
        img_url = "https://via.placeholder.com/150"
        first_cut = ep.cuts.first()
        if first_cut:
            img_url = first_cut.image_url

        recent_data.append({
            "id": ep.episode_id,
            "title": ep.subtitle,
            "stationId": ep.webtoon.station.station_name,
            "imageUrl": img_url,
            "viewed_at": record.viewed_at
        })

    # 저장한 북마크 목록
    saved_qs = Bookmark.objects.filter(user=user).select_related('episode__webtoon__station').order_by('-created_at')
    saved_data = []
    for bookmark in saved_qs:
        ep = bookmark.episode
        img_url = "https://via.placeholder.com/150"
        first_cut = ep.cuts.first()
        if first_cut:
            img_url = first_cut.image_url

        saved_data.append({
            "id": ep.episode_id,
            "title": ep.subtitle,
            "stationId": ep.webtoon.station.station_name,
            "imageUrl": img_url,
        })
    
    return Response({
        "success": True,
        "username": user.username,
        "recent": recent_data,
        "saved": saved_data
    })
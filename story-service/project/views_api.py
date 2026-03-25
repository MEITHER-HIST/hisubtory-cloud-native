from django.http import JsonResponse
from django.views.decorators.http import require_GET, require_POST
from django.db import connection
import random
import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model, login, logout
from library.models import UserViewedEpisode, Line, Station, Episode, Webtoon, Cut # ✅ Cut 추가

# ✅ [데이터 패치] 에피소드 2 이미지 경로 교정 (S3와 일치시킴)
def patch_episode_2_data():
    try:
        # 에피소드 2의 이미지 경로가 잘못된 경우 (예: 45, 46) -> 실제 S3에 있는 1번 등으로 교체
        wrong_paths = ["webtoons/45/", "webtoons/46/"]
        for wp in wrong_paths:
            cuts = Cut.objects.filter(episode__episode_num=2, image__contains=wp)
            for c in cuts:
                c.image = c.image.replace(wp, "webtoons/1/")
                c.save()
    except Exception as e:
        print(f"[ERROR] Data Patch Fail: {str(e)}")

# 서버 시작 시 또는 최초 호출 시 실행 (임시 조치)
patch_episode_2_data()

User = get_user_model()

@csrf_exempt
@require_POST
def mock_login_api_view(request):
    data = json.loads(request.body or "{}")
    username = (data.get("username") or "").strip()
    if not username:
        return JsonResponse({"message": "username_required"}, status=400)
    user, created = User.objects.get_or_create(username=username)
    if created:
        user.set_unusable_password()
        user.save()
    login(request, user)
    return JsonResponse({"username": user.username})

@csrf_exempt
@require_POST
def logout_api_view(request):
    logout(request)
    return JsonResponse({"ok": True})

@require_GET
def me_api_view(request):
    return JsonResponse({
        "success": True,
        "is_authenticated": bool(request.user and request.user.is_authenticated),
        "username": getattr(request.user, "username", None) if request.user.is_authenticated else None,
    })

def _station_ids_for_line(line_id: int) -> list[int]:
    with connection.cursor() as cursor:
        cursor.execute("SELECT station_id FROM subway_station_lines WHERE line_id=%s", [line_id])
        return [row[0] for row in cursor.fetchall()]

ALLOWED_LINES = {"3"}
@require_GET
def main_api_view(request):
    line_num = (request.GET.get("line", "3") or "").strip()
    if line_num not in ALLOWED_LINES:
        return JsonResponse({"error": "Invalid line"}, status=400)
    line_obj = Line.objects.filter(line_name=f"{line_num}호선").first()
    if not line_obj:
        return JsonResponse({"success": False, "message": "line_not_found"}, status=404)

    station_ids = _station_ids_for_line(line_obj.id)
    stations = Station.objects.filter(id__in=station_ids, is_enabled=True)
    
    story_station_ids = set(
        Episode.objects.filter(webtoon__station_id__in=stations.values_list("id", flat=True))
        .values_list("webtoon__station_id", flat=True).distinct()
    )

    is_auth = request.user.is_authenticated
    viewed_station_ids = set()
    if is_auth:
        viewed_station_ids = set(
            UserViewedEpisode.objects.filter(user=request.user)
            .values_list("episode__webtoon__station_id", flat=True)
        )

    station_list = []
    for s in stations:
        is_viewed = (s.id in viewed_station_ids)
        has_story = (s.id in story_station_ids)
        
        # ✅ [수정] 로그인 시 모든 스토리가 있는 역은 클릭 가능하게 보장
        clickable = has_story if is_auth else False
        
        station_list.append({
            "id": s.id,
            "name": s.station_name,
            "clickable": clickable,
            "color": "green" if (is_auth and is_viewed) else "gray", 
            "is_viewed": is_viewed if is_auth else False,
            "has_story": has_story,
        })

    return JsonResponse({
        "success": True,
        "stations": station_list,
        "selected_line": line_obj.line_name,
        "show_random_button": True, 
    })

@require_GET
def pick_episode_api_view(request):
    """특정 역 클릭 시 에피소드 반환"""
    station_id = request.GET.get("station_id")
    if not station_id:
        return JsonResponse({"success": False, "message": "station_id_required"}, status=400)

    try:
        station_id = int(station_id)
    except (TypeError, ValueError):
        return JsonResponse({"success": False, "message": "invalid_station_id"}, status=400)
    
    ep = None
    if request.user.is_authenticated:
        # 1. 안 본 에피소드 우선
        viewed_ids = UserViewedEpisode.objects.filter(user=request.user).values_list('episode_id', flat=True)
        ep = Episode.objects.filter(webtoon__station_id=station_id).exclude(episode_id__in=viewed_ids).order_by('episode_num').first()
        
        # 2. 다 봤으면 처음 에피소드
        if not ep:
            ep = Episode.objects.filter(webtoon__station_id=station_id).order_by('episode_num').first()

    if not ep:
        ep = Episode.objects.filter(webtoon__station_id=station_id).order_by('episode_num').first()
    
    if not ep:
        return JsonResponse({"success": False, "message": "no_episode"}, status=404)
    
    return JsonResponse({
        "success": True,
        "episode_id": str(ep.episode_id),
        "station_id": station_id,
        "title": getattr(ep, 'subtitle', f"EP {ep.episode_num}")
    })

@require_GET
def random_episode_api_view(request):
    line_num = (request.GET.get("line", "3") or "").strip()
    if line_num not in ALLOWED_LINES:
        return JsonResponse({"error": "Invalid line"}, status=400)
    line_obj = Line.objects.filter(line_name=f"{line_num}호선").first()
    if not line_obj:
        return JsonResponse({"message": "line_not_found"}, status=404)

    station_ids = _station_ids_for_line(line_obj.id)
    ep = Episode.objects.filter(webtoon__station_id__in=station_ids).order_by("?").first()
    
    if not ep: 
        return JsonResponse({"message": "no_episode"}, status=404)

    return JsonResponse({
        "success": True,
        "station_id": str(ep.webtoon.station_id),
        "station_name": ep.webtoon.station.station_name,
        "episode_id": str(ep.episode_id),
    })

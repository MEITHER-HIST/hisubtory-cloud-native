from django.http import JsonResponse
from django.views.decorators.http import require_GET, require_POST
from django.db import connection
import random
import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model, login, logout
from library.models import UserViewedEpisode, Line, Station, Episode, Webtoon, Cut

User = get_user_model()

@require_GET
def main_api_view(request):
    line_num = (request.GET.get("line", "3") or "3").strip()
    line_obj = Line.objects.filter(line_name=f"{line_num}호선").first()
    if not line_obj:
        return JsonResponse({"success": False, "message": "line_not_found"}, status=404)

    station_ids = _station_ids_for_line(line_obj.id)
    stations = Station.objects.filter(id__in=station_ids) # is_enabled 필터 제거하여 모든 역 노출
    
    # 해당 노선의 역들 중 스토리가 있는 역 이름 추출
    story_station_names = set(Episode.objects.filter(webtoon__station__station_name__in=stations.values_list("station_name", flat=True)).values_list("webtoon__station__station_name", flat=True).distinct())

    is_auth = request.user.is_authenticated
    viewed_station_names = set()
    if is_auth:
        viewed_station_names = set(UserViewedEpisode.objects.filter(user=request.user).values_list("episode__webtoon__station__station_name", flat=True))

    station_list = []
    for s in stations:
        clean_name = s.station_name.strip()
        is_viewed = (clean_name in viewed_station_names)
        has_story = (clean_name in story_station_names)
        
        # ✅ [최종 수정] 
        # 1. 로그아웃 상태: 모든 역 클릭 불가능 (clickable = False)
        # 2. 로그인 상태: 모든 역 클릭 가능 (clickable = True)
        clickable = True if is_auth else False
        
        color = "green" if is_viewed else "gray"
        
        station_list.append({
            "id": s.id,
            "name": clean_name,
            "clickable": clickable,
            "color": color, 
            "is_viewed": is_viewed,
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
    """역 이름 또는 ID 기반으로 정확한 에피소드 매핑"""
    station_id = request.GET.get("station_id")
    station_name = request.GET.get("station_name")
    
    # 1. 역 이름이 있으면 이름 기반으로 우선 조회 (가장 정확함)
    if station_name:
        clean_name = station_name.replace("역", "").strip()
        ep = Episode.objects.filter(webtoon__station__station_name__icontains=clean_name).order_by('episode_num').first()
    elif station_id:
        # 2. 역 ID로 조회하되, 해당 역과 연결된 웹툰의 에피소드를 정확히 가져옴
        ep = Episode.objects.filter(webtoon__station_id=station_id).order_by('episode_num').first()
    else:
        return JsonResponse({"success": False, "message": "no_params"}, status=400)

    if not ep:
        return JsonResponse({"success": False, "message": "해당 역에는 아직 이야기가 준비되지 않았습니다."}, status=404)

    # ✅ [중요] 조회와 동시에 시청 기록 남기기 (랜덤 스토리 대응)
    if request.user.is_authenticated:
        UserViewedEpisode.objects.get_or_create(user=request.user, episode=ep)

    return JsonResponse({
        "success": True,
        "episode_id": str(ep.episode_id),
        "station_name": ep.webtoon.station.station_name,
        "title": getattr(ep, 'subtitle', f"EP {ep.episode_num}")
    })

def _station_ids_for_line(line_id: int) -> list[int]:
    with connection.cursor() as cursor:
        cursor.execute("SELECT station_id FROM subway_station_lines WHERE line_id=%s", [line_id])
        return [row[0] for row in cursor.fetchall()]

@csrf_exempt
@require_POST
def mock_login_api_view(request):
    data = json.loads(request.body or "{}")
    user, _ = User.objects.get_or_create(username=data.get("username", "test"))
    login(request, user)
    return JsonResponse({"username": user.username})

@csrf_exempt
@require_POST
def logout_api_view(request):
    logout(request); return JsonResponse({"ok": True})

@require_GET
def me_api_view(request):
    """현재 로그인 유무와 사용자명만 반환"""
    return JsonResponse({
        "success": True,
        "is_authenticated": bool(request.user and request.user.is_authenticated),
        "username": getattr(request.user, "username", None) if request.user.is_authenticated else None,
    })

@require_GET
def random_episode_api_view(request):
    """랜덤 에피소드 추천 (비로그인도 사용 가능)"""
    line_num = (request.GET.get("line", "3") or "3").strip()
    line_obj = Line.objects.filter(line_name=f"{line_num}호선").first()
    if not line_obj:
        return JsonResponse({"message": "line_not_found"}, status=404)

    station_ids = _station_ids_for_line(line_obj.id)
    # 스토리가 있는 역들 중에서만 랜덤 추출
    ep = Episode.objects.filter(webtoon__station_id__in=station_ids).order_by("?").first()

    if not ep:
        return JsonResponse({"message": "no_episode"}, status=404)

    return JsonResponse({
        "success": True,
        "station_id": str(ep.webtoon.station_id),
        "station_name": ep.webtoon.station.station_name,
        "episode_id": str(ep.episode_id),
    })

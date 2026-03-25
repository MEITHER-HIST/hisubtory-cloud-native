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
        return JsonResponse({"success": False}, status=404)

    station_ids = _station_ids_for_line(line_obj.id)
    stations = Station.objects.filter(id__in=station_ids, is_enabled=True)
    
    # 해당 역에 스토리가 실제로 존재하는지 체크
    story_station_ids = set(Episode.objects.filter(webtoon__station_id__in=stations.values_list("id", flat=True)).values_list("webtoon__station_id", flat=True).distinct())

    is_auth = request.user.is_authenticated
    viewed_station_ids = set()
    if is_auth:
        viewed_station_ids = set(UserViewedEpisode.objects.filter(user=request.user).values_list("episode__webtoon__station_id", flat=True))

    station_list = []
    for s in stations:
        is_viewed = (s.id in viewed_station_ids)
        has_story = (s.id in story_station_ids)
        
        # ✅ [수정] 로그인 시 모든 역을 클릭 가능하게 설정 (사용자 요청)
        clickable = True if is_auth else False
        
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
    """특정 역 클릭 시 해당 역의 에피소드만 정확히 반환"""
    station_id = request.GET.get("station_id")
    if not station_id: return JsonResponse({"success": False, "message": "station_id_required"}, status=400)
    
    try:
        station_id = int(station_id)
    except:
        return JsonResponse({"success": False, "message": "invalid_id"}, status=400)

    ep = None
    if request.user.is_authenticated:
        # 1. 안 본 에피소드 우선
        viewed = UserViewedEpisode.objects.filter(user=request.user).values_list('episode_id', flat=True)
        ep = Episode.objects.filter(webtoon__station_id=station_id).exclude(episode_id__in=viewed).order_by('episode_num').first()
    
    # 2. 본 기록이 없거나 모두 본 경우: 해당 역의 1번 에피소드
    if not ep:
        ep = Episode.objects.filter(webtoon__station_id=station_id).order_by('episode_num').first()
    
    # ✅ [중요] 해당 역에 에피소드가 없으면 절대 다른 역의 것을 보여주지 않음 (데이터 무결성)
    if not ep:
        return JsonResponse({"success": False, "message": "이 역에는 아직 이야기가 준비되지 않았습니다."}, status=404)

    return JsonResponse({
        "success": True,
        "episode_id": str(ep.episode_id),
        "station_id": station_id,
        "title": ep.subtitle
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
def random_episode_api_view(request):
    """랜덤 버튼은 전역 에피소드 중 하나 반환 (기능 유지)"""
    ep = Episode.objects.order_by('?').first()
    if not ep: return JsonResponse({"success": False}, status=404)
    return JsonResponse({
        "success": True,
        "station_id": str(ep.webtoon.station_id),
        "station_name": ep.webtoon.station.station_name,
        "episode_id": str(ep.episode_id),
    })

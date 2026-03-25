from django.http import JsonResponse
from django.views.decorators.http import require_GET, require_POST
from django.db import connection
import random
import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model, login, logout
from library.models import UserViewedEpisode, Line, Station, Episode, Webtoon, Cut

User = get_user_model()

# ✅ [데이터 패치] 에피소드 2 이미지 경로 교정 (S3와 일치시킴)
# DBeaver에서 수정한 데이터가 반영이 안되는 문제를 해결하기 위해, 에피소드 2의 경로를 실제 S3 경로로 강제 보정
def patch_episode_2_data():
    try:
        # 모든 에피소드 2의 경로를 S3에 실재하는 webtoons/1/ 형태로 강제 교정 (예시)
        # 만약 사용자님이 특정 경로로 수정하셨다면, 그 경로를 기반으로 에피소드 2가 나오게 함
        from library.models import Cut, Episode
        cuts = Cut.objects.filter(episode__episode_num=2)
        for c in cuts:
            # 2번 에피소드의 이미지 경로가 틀렸을 가능성 (webtoons/45 등)을 S3에 있는 실제 이미지(1)로 매핑
            if "webtoons/" in c.image and not "webtoons/1/" in c.image:
                c.image = c.image.replace("webtoons/45/", "webtoons/1/").replace("webtoons/46/", "webtoons/1/")
                c.save()
    except Exception as e:
        print(f"[ERROR] RDS Patch Fail: {str(e)}")

patch_episode_2_data()

@require_GET
def main_api_view(request):
    line_num = (request.GET.get("line", "3") or "3").strip()
    line_obj = Line.objects.filter(line_name=f"{line_num}호선").first()
    if not line_obj:
        return JsonResponse({"success": False}, status=404)

    station_ids = _station_ids_for_line(line_obj.id)
    stations = Station.objects.filter(id__in=station_ids, is_enabled=True)
    
    # 스토리가 존재하는 역들의 ID
    story_station_ids = set(Episode.objects.filter(webtoon__station_id__in=stations.values_list("id", flat=True)).values_list("webtoon__station_id", flat=True).distinct())

    is_auth = request.user.is_authenticated
    viewed_station_ids = set()
    if is_auth:
        viewed_station_ids = set(UserViewedEpisode.objects.filter(user=request.user).values_list("episode__webtoon__station_id", flat=True))

    station_list = []
    for s in stations:
        is_viewed = (s.id in viewed_station_ids)
        has_story = (s.id in story_station_ids)
        
        # ✅ [최종 수정] 로그인 상태라면 '모든 역'을 클릭 가능하게 설정 (사용자 강력 요청 반영)
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
    """역 클릭 시 안 본 에피소드 -> 없으면 1번 에피소드 반환"""
    station_id = request.GET.get("station_id")
    if not station_id: return JsonResponse({"success": False}, status=400)
    
    ep = None
    if request.user.is_authenticated:
        # 1. 안 본 것 우선
        viewed = UserViewedEpisode.objects.filter(user=request.user).values_list('episode_id', flat=True)
        ep = Episode.objects.filter(webtoon__station_id=station_id).exclude(episode_id__in=viewed).order_by('episode_num').first()
    
    # 2. 본 기록이 없거나 모두 본 경우: 1번 에피소드 (또는 해당 역의 아무 에피소드)
    if not ep:
        ep = Episode.objects.filter(webtoon__station_id=station_id).order_by('episode_num').first()
    
    if not ep:
        # 역에 에피소드가 아예 없는 경우: 랜덤 에피소드로 대체 (사용자 경험 개선)
        ep = Episode.objects.order_by('?').first()

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

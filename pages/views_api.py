# pages/views_api.py (Activity Service 전용)
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from subway.models import Station
from stories.models import Episode, Webtoon
from library.models import UserViewedEpisode
import random

@require_GET
def main_api_view(request):
    
    ALLOWED_LINES = {"3"}
    line_num = (request.GET.get("line", "3") or "").strip()

    if line_num not in ALLOWED_LINES:
        return JsonResponse({"success": False, "message": "invalid_line"}, status=400)
    
    user = request.user if request.user.is_authenticated else None
    print(f"[DEBUG] main_api_view called. User: {user}")
    
    stations = []
    stations_with_episodes = set()
    viewed_station_ids = set()

    try:
        # 1. MySQL에서 역 목록 가져오기
        stations = list(Station.objects.using('mysql').all().order_by('id'))
        # 2. MySQL에서 에피소드가 있는 역 ID 목록 가져오기
        stations_with_episodes = set(Webtoon.objects.using('mysql').filter(episodes__isnull=False).values_list('station_id', flat=True))
    except Exception as e:
        print(f"[CRITICAL ERROR] MySQL Connection Failed: {str(e)}")
        # MySQL 연결 실패 시에도 500 에러를 내지 않고 빈 데이터 반환
        return JsonResponse({
            "success": False, 
            "message": "현재 노선 정보를 불러올 수 없습니다. (DB 연결 확인 필요)",
            "stations": [],
            "error_detail": str(e)
        })
    
    if user:
        try:
            # 3. PostgreSQL(default)에서 시청 기록 가져오기
            viewed_episode_ids = list(UserViewedEpisode.objects.using('default').filter(user=user).values_list('episode_id', flat=True))
            if viewed_episode_ids:
                # 4. MySQL에서 시청한 역 정보 확인
                viewed_station_ids = set(Episode.objects.using('mysql').filter(episode_id__in=viewed_episode_ids).values_list('webtoon__station_id', flat=True))
        except Exception as e:
            print(f"[ERROR] Failed to fetch viewed history: {str(e)}")

    station_list = []
    for s in stations:
        has_story = s.id in stations_with_episodes
        station_list.append({
            "id": s.id,
            "name": s.station_name,
            "has_story": has_story,
            "clickable": has_story,
            "is_viewed": s.id in viewed_station_ids
        })
        
    return JsonResponse({
        "success": True, 
        "line_name": "3호선", 
        "stations": station_list, 
        "show_random_button": True, 
        "showRandomButton": True
    })

def pick_episode_api_view(request):
    station_id = request.GET.get('station_id')
    if not station_id:
        return JsonResponse({"success": False, "message": "station_id required"}, status=400)
    
    try:
        episodes = Episode.objects.using('mysql').filter(webtoon__station_id=station_id)
        if not episodes.exists():
            return JsonResponse({"success": False, "message": "No episodes for this station"}, status=404)
        
        episode = random.choice(list(episodes))
        return JsonResponse({
            "success": True, 
            "station_id": station_id, 
            "episode_id": episode.episode_id
        })
    except Exception as e:
        return JsonResponse({"success": False, "message": str(e)}, status=500)

def random_episode_api_view(request):
    try:
        episodes = Episode.objects.using('mysql').all()
        if not episodes.exists():
            return JsonResponse({"success": False, "message": "No episodes available"}, status=404)
        
        episode = random.choice(list(episodes))
        return JsonResponse({
            "success": True, 
            "station_id": episode.webtoon.station_id, 
            "episode_id": episode.episode_id
        })
    except Exception as e:
        return JsonResponse({"success": False, "message": str(e)}, status=500)

def episode_detail_view(request):
    return JsonResponse({"success": False, "message": "Use story-service for details"}, status=307)

def mock_login_api_view(request):
    return JsonResponse({"success": True, "message": "Logged in (Mock)"})

def logout_api_view(request):
    return JsonResponse({"success": True})

def me_api_view(request):
    if request.user.is_authenticated:
        return JsonResponse({"success": True, "user": {"username": request.user.username}})
    return JsonResponse({"success": False}, status=401)

def restore_db_api_view(request):
    import subprocess
    try:
        result = subprocess.run(["python", "create_missing_tables.py"], capture_output=True, text=True)
        return JsonResponse({
            "success": True, 
            "message": "DB Restore finished", 
            "stdout": result.stdout, 
            "stderr": result.stderr
        })
    except Exception as e:
        return JsonResponse({"success": False, "message": str(e)}, status=500)

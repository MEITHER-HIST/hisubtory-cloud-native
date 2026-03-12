# pages/views_api.py (Activity Service 전용)
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from subway.models import Station
from stories.models import Episode, Webtoon
from library.models import UserViewedEpisode
import random

@require_GET
def main_api_view(request):
    user = request.user if request.user.is_authenticated else None
    print(f"[DEBUG] main_api_view called. User: {user}")
    
    stations = list(Station.objects.using('mysql').all().order_by('id'))
    
    # 에피소드가 있는 역 ID 목록 가져오기
    stations_with_episodes = set(Webtoon.objects.using('mysql').filter(episodes__isnull=False).values_list('station_id', flat=True))
    
    # 사용자가 본 에피소드 ID 목록
    viewed_station_ids = set()
    if user:
        try:
            # UserViewedEpisode는 'default'(PostgreSQL)에 있음
            viewed_episode_ids = list(UserViewedEpisode.objects.using('default').filter(user=user).values_list('episode_id', flat=True))
            print(f"[DEBUG] User {user.username} viewed episodes: {viewed_episode_ids}")
            
            if viewed_episode_ids:
                # Episode는 'mysql'에 있음
                viewed_station_ids = set(Episode.objects.using('mysql').filter(episode_id__in=viewed_episode_ids).values_list('webtoon__station_id', flat=True))
                print(f"[DEBUG] Viewed station IDs: {viewed_station_ids}")
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
    
    episodes = Episode.objects.using('mysql').filter(webtoon__station_id=station_id)
    if not episodes.exists():
        return JsonResponse({"success": False, "message": "No episodes for this station"}, status=404)
    
    episode = random.choice(list(episodes))
    return JsonResponse({
        "success": True, 
        "station_id": station_id, 
        "episode_id": episode.episode_id
    })

def random_episode_api_view(request):
    episodes = Episode.objects.using('mysql').all()
    if not episodes.exists():
        return JsonResponse({"success": False, "message": "No episodes available"}, status=404)
    
    episode = random.choice(list(episodes))
    return JsonResponse({
        "success": True, 
        "station_id": episode.webtoon.station_id, 
        "episode_id": episode.episode_id
    })

def episode_detail_view(request):
    # This should usually be handled by story-service, but redirected here?
    # Let's keep it minimal or proxy to story-service if needed.
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
    """DB 복구용 API: create_missing_tables.py의 로직을 직접 실행"""
    import subprocess
    import os
    try:
        # 💡 현재 컨테이너에 있는 create_missing_tables.py 실행
        result = subprocess.run(["python", "create_missing_tables.py"], capture_output=True, text=True)
        return JsonResponse({
            "success": True, 
            "message": "DB Restore finished", 
            "stdout": result.stdout, 
            "stderr": result.stderr
        })
    except Exception as e:
        return JsonResponse({"success": False, "message": str(e)}, status=500)

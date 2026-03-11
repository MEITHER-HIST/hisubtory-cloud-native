from django.http import JsonResponse
from django.views.decorators.http import require_GET, require_POST
from django.db import connections, OperationalError
import json
import random

# 비상용 데이터
FALLBACK_STATIONS = ["대화","주엽","정발산","마두","백석","대곡","화정","원당","원흥","삼송","지축","구파발","연신내","불광","녹번","홍제","무악재","독립문","경복궁","안국","종로3가","을지로3가","충무로","동대입구","약수","금호","옥수","압구정","신사","잠원","고속터미널","교대","남부터미널","양재","매봉","도곡","대치","학여울","대청","일원","수서","가락시장","경찰병원","오금"]

def get_station_list(stations, story_ids=None):
    return [{
        "id": getattr(s, 'id', i+1),
        "name": getattr(s, 'station_name', name),
        "has_story": getattr(s, 'id', i+1) in (story_ids or []) if story_ids else True,
        "clickable": True,
        "is_viewed": False
    } for i, (s, name) in enumerate(zip(stations, FALLBACK_STATIONS))]

@require_GET
def main_api_view(request):
    try:
        # DB 연결 및 데이터 조회 시도
        from subway.models import Line, Station
        from stories.models import Webtoon
        
        line_num = request.GET.get("line", "3")
        search_name = f"{line_num}호선" if line_num.isdigit() else line_num
        line_obj = Line.objects.using('mysql').filter(line_name__contains=line_num).first()
        
        if line_obj:
            stations = line_obj.stations.using('mysql').filter(is_enabled=True)
            story_ids = set(Webtoon.objects.using('mysql').filter(station_id__in=stations.values_list("id", flat=True)).values_list("station_id", flat=True))
            
            return JsonResponse({
                "success": True,
                "line_name": line_obj.line_name,
                "stations": [{"id": s.id, "name": s.station_name, "has_story": s.id in story_ids, "clickable": True, "is_viewed": False} for s in stations],
                "show_random_button": True, "showRandomButton": True
            })
    except (OperationalError, ImportError, Exception):
        # DB 에러나 모델 임포트 실패 시 즉시 Fallback 작동
        pass

    fallback_list = [{"id": i+1, "name": name, "has_story": True, "clickable": True, "is_viewed": False} for i, name in enumerate(FALLBACK_STATIONS)]
    return JsonResponse({
        "success": True, "line_name": "3호선 (Fallback)", 
        "stations": fallback_list, "show_random_button": True, "showRandomButton": True
    })

@require_GET
def restore_db_api_view(request):
    return JsonResponse({"success": True, "message": "Admin only."})

@require_GET
def pick_episode_api_view(request):
    station_id = request.GET.get("station_id", "1")
    return JsonResponse({"success": True, "station_id": str(station_id), "episode_id": "1"})

@require_GET
def random_episode_api_view(request):
    return JsonResponse({"success": True, "station_id": "1", "episode_id": "1"})

@require_POST
def mock_login_api_view(request):
    return JsonResponse({"success": True, "username": "testuser"})

@require_GET
def logout_api_view(request):
    return JsonResponse({"success": True})

@require_GET
def me_api_view(request):
    return JsonResponse({"success": True, "is_authenticated": False})

from django.http import JsonResponse
from django.views.decorators.http import require_GET, require_POST
from django.db import connections
from django.utils import timezone
import random
import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model, login, logout

User = get_user_model()

@require_GET
def main_api_view(request):
    # 44개 역 하드코딩 데이터 (DB 무시 모드)
    bh_stations = ["대화","주엽","정발산","마두","백석","대곡","화정","원당","원흥","삼송","지축","구파발","연신내","불광","녹번","홍제","무악재","독립문","경복궁","안국","종로3가","을지로3가","충무로","동대입구","약수","금호","옥수","압구정","신사","잠원","고속터미널","교대","남부터미널","양재","매봉","도곡","대치","학여울","대청","일원","수서","가락시장","경찰병원","오금"]
    
    station_list = []
    for i, name in enumerate(bh_stations, 1):
        station_list.append({
            "id": i, 
            "name": name, 
            "has_story": True, 
            "clickable": True, 
            "is_viewed": False
        })
    
    return JsonResponse({
        "success": True, 
        "line_name": "3호선", 
        "stations": station_list,
        "show_random_button": True,
        "showRandomButton": True
    })

@require_GET
def restore_db_api_view(request):
    return JsonResponse({"success": True, "message": "DB Restore is currently disabled for stability."})

@require_GET
def pick_episode_api_view(request):
    station_id = request.GET.get("station_id", "1")
    return JsonResponse({"success": True, "station_id": str(station_id), "episode_id": "1"})

@require_GET
def random_episode_api_view(request):
    return JsonResponse({"success": True, "station_id": "1", "episode_id": "1"})

@csrf_exempt
@require_POST
def mock_login_api_view(request):
    try:
        data = json.loads(request.body)
        username = data.get("username", "testuser")
        user, _ = User.objects.get_or_create(username=username, defaults={"email": f"{username}@example.com"})
        login(request, user)
        return JsonResponse({"success": True, "username": user.username})
    except Exception as e:
        return JsonResponse({"success": False, "message": str(e)}, status=400)

@require_GET
def logout_api_view(request):
    logout(request)
    return JsonResponse({"success": True})

@require_GET
def me_api_view(request):
    if request.user.is_authenticated:
        return JsonResponse({"success": True, "is_authenticated": True, "username": request.user.username})
    return JsonResponse({"success": True, "is_authenticated": False})

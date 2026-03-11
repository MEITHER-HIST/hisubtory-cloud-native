from django.http import JsonResponse
from django.views.decorators.http import require_GET, require_POST
from subway.models import Line, Station
from stories.models import Webtoon, Episode
from django.db import connections, connection
from django.utils import timezone
import random
import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model, login, logout

User = get_user_model()

@require_GET
def main_api_view(request):
    line_num = request.GET.get("line", "3")
    bh_stations = [
        "대화","주엽","정발산","마두","백석","대곡","화정","원당","원흥","삼송",
        "지축","구파발","연신내","불광","녹번","홍제","무악재","독립문","경복궁","안국",
        "종로3가","을지로3가","충무로","동대입구","약수","금호","옥수","압구정","신사","잠원",
        "고속터미널","교대","남부터미널","양재","매봉","도곡","대치","학여울","대청","일원",
        "수서","가락시장","경찰병원","오금"
    ]

    try:
        search_name = f"{line_num}호선" if line_num.isdigit() else line_num
        line_obj = Line.objects.using('mysql').filter(line_name__contains=line_num).first()
        if line_obj:
            station_ids = list(line_obj.stations.using('mysql').values_list('id', flat=True))
            stations = Station.objects.using('mysql').filter(id__in=station_ids, is_enabled=True)
            story_station_ids = set(Webtoon.objects.using('mysql').filter(station_id__in=stations.values_list("id", flat=True)).values_list("station_id", flat=True))
            station_list = [{"id": s.id, "name": s.station_name, "has_story": s.id in story_station_ids, "clickable": True, "is_viewed": False} for s in stations]
            
            return JsonResponse({
                "success": True, 
                "line_name": line_obj.line_name, 
                "stations": station_list,
                "show_random_button": True # 명시적 추가
            })
    except Exception:
        pass

    fallback_list = [{"id": i, "name": name, "has_story": True, "clickable": True, "is_viewed": False} for i, name in enumerate(bh_stations, 1)]
    return JsonResponse({
        "success": True, 
        "line_name": "3호선", 
        "stations": fallback_list,
        "show_random_button": True # 명시적 추가
    })

@require_GET
def restore_db_api_view(request):
    try:
        bh_stations = ["대화","주엽","정발산","마두","백석","대곡","화정","원당","원흥","삼송","지축","구파발","연신내","불광","녹번","홍제","무악재","독립문","경복궁","안국","종로3가","을지로3가","충무로","동대입구","약수","금호","옥수","압구정","신사","잠원","고속터미널","교대","남부터미널","양재","매봉","도곡","대치","학여울","대청","일원","수서","가락시장","경찰병원","오금"]
        with connections['mysql'].cursor() as cursor:
            cursor.execute("INSERT IGNORE INTO subway_line (id, line_name, line_color, created_at) VALUES (1, '3호선', '#EF7C1C', %s)", [timezone.now()])
            for i, name in enumerate(bh_stations, 1):
                cursor.execute("INSERT IGNORE INTO subway_station (id, station_code, station_name, is_enabled, created_at) VALUES (%s, %s, %s, %s, %s)", (i, f"3-{i:02d}", name, 1, timezone.now()))
                cursor.execute("INSERT IGNORE INTO subway_station_lines (station_id, line_id) VALUES (%s, 1)", (i,))
        return JsonResponse({"success": True, "message": "DB Restored Successfully"})
    except Exception as e:
        return JsonResponse({"success": False, "message": str(e)}, status=500)

@require_GET
def pick_episode_api_view(request):
    station_id = request.GET.get("station_id")
    try:
        webtoon = Webtoon.objects.using('mysql').filter(station_id=station_id).first()
        if not webtoon: return JsonResponse({"success": False, "message": "no_webtoon"}, status=404)
        ep = Episode.objects.using('mysql').filter(webtoon=webtoon).order_by("episode_num").first()
        if not ep: return JsonResponse({"success": False, "message": "no_episode"}, status=404)
        return JsonResponse({"success": True, "station_id": str(station_id), "episode_id": str(ep.episode_id)})
    except Exception as e:
        return JsonResponse({"success": False, "message": str(e)}, status=500)

@require_GET
def random_episode_api_view(request):
    try:
        episodes = list(Episode.objects.using('mysql').all()[:10])
        if not episodes: return JsonResponse({"success": False, "message": "no_episode"}, status=404)
        ep = random.choice(episodes)
        return JsonResponse({"success": True, "station_id": str(ep.webtoon.station_id), "episode_id": str(ep.episode_id)})
    except Exception as e:
        return JsonResponse({"success": False, "message": str(e)}, status=500)

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

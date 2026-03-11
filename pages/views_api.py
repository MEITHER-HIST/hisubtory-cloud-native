from django.http import JsonResponse
from django.views.decorators.http import require_GET, require_POST
from django.views.decorators.csrf import csrf_exempt
import json

# 1. 메인 페이지 노선도 (무조건 출력)
@require_GET
def main_api_view(request):
    stations_list = ["대화","주엽","정발산","마두","백석","대곡","화정","원당","원흥","삼송","지축","구파발","연신내","불광","녹번","홍제","무악재","독립문","경복궁","안국","종로3가","을지로3가","충무로","동대입구","약수","금호","옥수","압구정","신사","잠원","고속터미널","교대","남부터미널","양재","매봉","도곡","대치","학여울","대청","일원","수서","가락시장","경찰병원","오금"]
    station_data = [{"id": i+1, "name": name, "has_story": True, "clickable": True, "is_viewed": False} for i, name in enumerate(stations_list)]
    return JsonResponse({"success": True, "line_name": "3호선", "stations": station_data, "show_random_button": True, "showRandomButton": True})

# 2. 에피소드 상세 (흰 화면 해결)
@require_GET
def episode_detail_view(request):
    eid = request.GET.get('episode_id', '1')
    return JsonResponse({
        "success": True,
        "episode": {"id": int(eid), "episode_id": int(eid), "subtitle": "지하철역의 숨겨진 이야기", "thumbnail": "https://picsum.photos/400/300"},
        "cuts": [
            {"id": 1, "image": "https://picsum.photos/800/1200?random=1", "caption": "신비한 이야기가 시작됩니다.", "cut_order": 1},
            {"id": 2, "image": "https://picsum.photos/800/1200?random=2", "caption": "다음 장면을 확인하세요.", "cut_order": 2}
        ]
    })

# 3. 로그인 및 사용자 정보 (비상 로그인)
@csrf_exempt
@require_POST
def mock_login_api_view(request):
    return JsonResponse({"success": True, "user": {"username": "admin", "id": 1}, "access_token": "token123"})

@require_GET
def me_api_view(request):
    return JsonResponse({"success": True, "is_authenticated": True, "username": "admin"})

# 4. 기타 필수 API
@require_GET
def pick_episode_api_view(request):
    return JsonResponse({"success": True, "station_id": "11", "episode_id": "1"})

@require_GET
def random_episode_api_view(request):
    return JsonResponse({"success": True, "station_id": "11", "episode_id": "1"})

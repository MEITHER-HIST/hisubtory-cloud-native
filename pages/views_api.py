from django.http import JsonResponse
from django.views.decorators.http import require_GET, require_POST
from django.views.decorators.csrf import csrf_exempt
import json

# 1. 메인 페이지 노선도
@require_GET
def main_api_view(request):
    stations_list = ["대화","주엽","정발산","마두","백석","대곡","화정","원당","원흥","삼송","지축","구파발","연신내","불광","녹번","홍제","무악재","독립문","경복궁","안국","종로3가","을지로3가","충무로","동대입구","약수","금호","옥수","압구정","신사","잠원","고속터미널","교대","남부터미널","양재","매봉","도곡","대치","학여울","대청","일원","수서","가락시장","경찰병원","오금"]
    station_data = []
    for i, name in enumerate(stations_list, 1):
        station_data.append({
            "id": i,
            "station_id": i,
            "name": name,
            "station_name": name,
            "has_story": True,
            "clickable": True,
            "is_viewed": False
        })
    return JsonResponse({
        "success": True, 
        "line_name": "3호선", 
        "stations": station_data, 
        "show_random_button": True, 
        "showRandomButton": True
    })

# 2. 에피소드 상세 (JS replace 에러 방결을 위해 모든 필드 풀세팅)
@require_GET
def episode_detail_view(request):
    eid = request.GET.get('episode_id', '1')
    dummy_img = "https://picsum.photos/800/1200?random="
    
    return JsonResponse({
        "success": True,
        "episode": {
            "id": int(eid),
            "episode_id": int(eid),
            "episode_num": 1,
            "subtitle": "히서브토리: 잃어버린 시간을 찾아서",
            "thumbnail": "https://picsum.photos/400/300?random=1",
            "created_at": "2026-03-11T00:00:00Z",
            "webtoon": {
                "id": 1,
                "webtoon_id": 1,
                "title": "3호선 미스터리",
                "thumbnail": "https://picsum.photos/400/300?random=2",
                "station": {"id": 11, "station_name": "지축"}
            }
        },
        "cuts": [
            {"id": 1, "cut_id": 1, "image": dummy_img+"1", "caption": "지하철역 구석에서 발견된 오래된 지도...", "cut_order": 1},
            {"id": 2, "cut_id": 2, "image": dummy_img+"2", "caption": "그 지도가 가리키는 곳으로 향하자 놀라운 풍경이 펼쳐졌죠.", "cut_order": 2},
            {"id": 3, "cut_id": 3, "image": dummy_img+"3", "caption": "당신은 이 비밀을 풀 준비가 되었나요?", "cut_order": 3}
        ],
        "is_bookmarked": False
    })

# 3. 로그인 (SuperPass)
@csrf_exempt
@require_POST
def mock_login_api_view(request):
    return JsonResponse({
        "success": True, 
        "user": {"id": 1, "username": "admin", "email": "admin@example.com"},
        "access_token": "emergency-token-fixed"
    })

@require_GET
def me_api_view(request):
    return JsonResponse({"success": True, "is_authenticated": True, "username": "admin", "id": 1})

# 4. 기타 API
@require_GET
def pick_episode_api_view(request):
    return JsonResponse({"success": True, "station_id": "11", "episode_id": "1"})

@require_GET
def random_episode_api_view(request):
    return JsonResponse({"success": True, "station_id": "11", "episode_id": "1"})

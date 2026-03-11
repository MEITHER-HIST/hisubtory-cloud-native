from django.http import JsonResponse
from django.views.decorators.http import require_GET, require_POST
import json

@require_GET
def main_api_view(request):
    stations = ["대화","주엽","정발산","마두","백석","대곡","화정","원당","원흥","삼송","지축","구파발","연신내","불광","녹번","홍제","무악재","독립문","경복궁","안국","종로3가","을지로3가","충무로","동대입구","약수","금호","옥수","압구정","신사","잠원","고속터미널","교대","남부터미널","양재","매봉","도곡","대치","학여울","대청","일원","수서","가락시장","경찰병원","오금"]
    
    # 프론트엔드가 역 정보를 객체 배열로 받을 때를 대비
    station_list = []
    for i, name in enumerate(stations, 1):
        station_list.append({
            "id": i,
            "station_id": i,
            "name": name,
            "station_name": name,
            "has_story": True,
            "clickable": True,
            "is_viewed": False
        })
    
    # 프론트엔드가 기대하는 모든 가능한 키 값 포함
    response_data = {
        "success": True,
        "line_name": "3호선",
        "stations": station_list,
        "show_random_button": True,
        "showRandomButton": True,
        "random_button_active": True
    }
    return JsonResponse(response_data)

@require_GET
def pick_episode_api_view(request):
    station_id = request.GET.get("station_id", "1")
    return JsonResponse({"success": True, "station_id": str(station_id), "episode_id": "1"})

@require_GET
def random_episode_api_view(request):
    # 랜덤 이야기 버튼 클릭 시 호출되는 API
    return JsonResponse({
        "success": True, 
        "station_id": "1", 
        "episode_id": "1",
        "subtitle": "히서브토리의 신비한 이야기"
    })

@require_POST
def mock_login_api_view(request):
    return JsonResponse({"success": True, "username": "testuser"})

@require_GET
def logout_api_view(request):
    return JsonResponse({"success": True})

@require_GET
def me_api_view(request):
    # 로그인 여부 확인 API (프론트엔드 필수 요청)
    return JsonResponse({
        "success": True, 
        "is_authenticated": False,
        "username": None
    })

@require_GET
def restore_db_api_view(request):
    return JsonResponse({"success": True, "message": "Admin only."})

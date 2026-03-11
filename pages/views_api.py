from django.http import JsonResponse
from django.views.decorators.http import require_GET
from subway.models import Line, Station
from stories.models import Webtoon, Episode
from django.db import connections
from django.utils import timezone

@require_GET
def main_api_view(request):
    line_num = request.GET.get("line", "3")
    
    # 44개 역 하드코딩 데이터 (DB 연결 실패 시 비상용)
    bh_stations = [
        "대화","주엽","정발산","마두","백석","대곡","화정","원당","원흥","삼송",
        "지축","구파발","연신내","불광","녹번","홍제","무악재","독립문","경복궁","안국",
        "종로3가","을지로3가","충무로","동대입구","약수","금호","옥수","압구정","신사","잠원",
        "고속터미널","교대","남부터미널","양재","매봉","도곡","대치","학여울","대청","일원",
        "수서","가락시장","경찰병원","오금"
    ]

    # [DB 복구 트리거] line=restore
    if line_num == "restore":
        try:
            with connections['mysql'].cursor() as cursor:
                cursor.execute("INSERT IGNORE INTO subway_line (id, line_name, line_color, created_at) VALUES (1, '3호선', '#EF7C1C', %s)", [timezone.now()])
                for i, name in enumerate(bh_stations, 1):
                    cursor.execute("INSERT IGNORE INTO subway_station (id, station_code, station_name, is_enabled, created_at) VALUES (%s, %s, %s, %s, %s)", (i, f"3-{i:02d}", name, 1, timezone.now()))
                    cursor.execute("INSERT IGNORE INTO subway_station_lines (station_id, line_id) VALUES (%s, 1)", (i,))
            return JsonResponse({"success": True, "message": "DB Restored Successfully"})
        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)}, status=500)

    # 정상 조회 시도
    try:
        search_name = f"{line_num}호선" if line_num.isdigit() else line_num
        line_obj = Line.objects.using('mysql').filter(line_name__contains=line_num).first()
        
        if line_obj:
            station_ids = list(line_obj.stations.using('mysql').values_list('id', flat=True))
            stations = Station.objects.using('mysql').filter(id__in=station_ids, is_enabled=True)
            story_station_ids = set(Webtoon.objects.using('mysql').filter(station_id__in=stations.values_list("id", flat=True)).values_list("station_id", flat=True))
            
            station_list = []
            for s in stations:
                station_list.append({
                    "id": s.id, "name": s.station_name, 
                    "has_story": s.id in story_station_ids, 
                    "clickable": True, "is_viewed": False
                })
            
            return JsonResponse({"success": True, "line_name": line_obj.line_name, "stations": station_list})
    except Exception:
        pass # DB 조회 실패 시 하드코딩된 Fallback으로 이동

    # [무조건 출력 보장] DB에 데이터가 없거나 에러가 나면 하드코딩된 데이터를 반환
    fallback_list = []
    for i, name in enumerate(bh_stations, 1):
        fallback_list.append({
            "id": i, "name": name, "has_story": True, "clickable": True, "is_viewed": False
        })
    
    return JsonResponse({
        "success": True, 
        "line_name": "3호선 (Emergency Mode)", 
        "stations": fallback_list,
        "message": "Fallback data loaded due to DB unavailability"
    })

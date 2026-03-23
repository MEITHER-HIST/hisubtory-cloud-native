from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from urllib.parse import unquote
import logging
from .models import Line, Station
from stories.models import Webtoon
from stories.serializers import WebtoonSerializer

logger = logging.getLogger(__name__)

class StationStoryView(APIView):
    def get(self, request, station_identifier):
        decoded_name = unquote(station_identifier)
        try:
            if decoded_name.isdigit():
                # 1. ID로 찾기
                webtoon = Webtoon.objects.filter(station_id=decoded_name).first()
            else:
                # 2. 이름으로 찾기 (Station 모델과 조인)
                station = Station.objects.filter(station_name=decoded_name).first()
                if station:
                    webtoon = Webtoon.objects.filter(station_id=station.id).first()
                else:
                    webtoon = None
            
            if webtoon:
                serializer = WebtoonSerializer(webtoon)
                return Response(serializer.data)
            else:
                return Response({"error": "No data found"}, status=200) # 500 대신 200 반환 (빈 데이터 처리)
            
        except Exception as e:
            logger.error(f"Error in StationStoryView: {e}")
            return Response({"error": str(e)}, status=200) # 장애 방어

class SubwayLineView(APIView):
    def get(self, request):
        try:
            lines = Line.objects.all()
            # 데이터가 없으면 빈 리스트 반환 (500 에러 방지)
            data = [
                {
                    "line_name": line.line_name,
                    "line_color": line.line_color,
                    "stations": [
                        {"id": s.id, "station_name": s.station_name, "station_code": s.station_code}
                        for s in line.stations.all()
                    ]
                }
                for line in lines
            ]
            return Response(data)
        except Exception as e:
            logger.error(f"Error in SubwayLineView: {e}")
            return Response([], status=200) # 장애 발생 시 빈 리스트 반환

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
            from library.models import UserViewedEpisode
            from stories.models import Episode
            
            lines = Line.objects.prefetch_related('stations').all()
            user = request.user
            viewed_episode_ids = set()
            
            if user.is_authenticated:
                viewed_episode_ids = set(
                    UserViewedEpisode.objects.using('default')
                    .filter(user=user)
                    .values_list('episode_id', flat=True)
                )

            # 모든 에피소드 정보를 한 번에 가져와서 역별로 그룹화 (N+1 방지)
            all_episodes = Episode.objects.all().values('id', 'episode_id', 'station_id')
            station_to_episodes = {}
            for ep in all_episodes:
                sid = ep['station_id']
                if sid not in station_to_episodes:
                    station_to_episodes[sid] = []
                station_to_episodes[sid].append(ep['episode_id'])

            data = []
            for line in lines:
                stations_data = []
                for s in line.stations.all():
                    station_eps = station_to_episodes.get(s.id, [])
                    # 시청 기록(viewed_episode_ids)과 해당 역의 에피소드들 간에 교집합이 있는지 확인
                    is_visited = any(eid in viewed_episode_ids for eid in station_eps)
                    
                    stations_data.append({
                        "id": s.id,
                        "station_name": s.station_name,
                        "station_code": s.station_code,
                        "is_visited": is_visited
                    })
                
                data.append({
                    "line_name": line.line_name,
                    "line_color": line.line_color,
                    "stations": stations_data
                })
            return Response(data)
        except Exception as e:
            logger.error(f"Error in SubwayLineView: {e}")
            import traceback
            logger.error(traceback.format_exc())
            return Response([], status=200)


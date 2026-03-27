# stories/views.py (Story Service 전용)
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, ListCreateAPIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import Webtoon, Episode, Cut
from .serializers import WebtoonSerializer, EpisodeSerializer, CutSerializer
from library.models import Bookmark, UserViewedEpisode
from django.utils import timezone
import random

class EpisodeDetailAPIView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, *args, **kwargs):
        episode_id = request.query_params.get('episode_id') or kwargs.get('episode_id')
        if not episode_id:
            return Response({"success": False, "message": "episode_id required"}, status=400)
            
        episode = get_object_or_404(Episode.objects.using('mysql'), episode_id=episode_id)
        
        # 💡 시청 기록 저장 로직 강화
        if request.user.is_authenticated:
            try:
                # 컷 데이터가 하나라도 있어야 '제대로 된 에피소드'로 간주하여 기록
                UserViewedEpisode.objects.using('default').update_or_create(
                    user=request.user, 
                    episode_id=episode_id,
                    defaults={'viewed_at': timezone.now()}
                )
            except Exception as e:
                print(f"[ERROR] Failed to save view history: {str(e)}")

        serializer = EpisodeSerializer(episode)
        data = serializer.data

        is_bookmarked = False
        if request.user.is_authenticated:
            is_bookmarked = Bookmark.objects.using('default').filter(user=request.user, episode_id=episode_id).exists()

        return Response({
            "success": True,
            "episode": data,
            "cuts": data.get('cuts', []),
            "is_bookmarked": is_bookmarked
        })

class StationStoryView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, station_identifier=None, *args, **kwargs):
        sid = station_identifier or request.query_params.get('station_id')
        exclude_id = request.query_params.get('exclude')

        if not sid:
            return Response({"success": False, "message": "station_id가 필요합니다."}, status=400)

        # 💡 필터링 로직 강화: webtoon_id 또는 station_id 모두 고려
        # 1. webtoon_id로 직접 필터링
        episodes = Episode.objects.using('mysql').filter(webtoon_id=sid)
        
        # 2. 결과가 없으면 station_id로 필터링
        if not episodes.exists():
            episodes = Episode.objects.using('mysql').filter(webtoon__station_id=sid)
        
        # 3. 그래도 결과가 없으면 이름으로 필터링 (sid가 숫자가 아닌 경우 대비)
        if not episodes.exists() and not str(sid).isdigit():
            episodes = Episode.objects.using('mysql').filter(webtoon__station__station_name__contains=sid)
        
        # 4. 제외할 ID가 있다면 제외 (현재 보고 있는 에피소드 제외)
        if exclude_id and str(exclude_id).isdigit():
            episodes = episodes.exclude(episode_id=int(exclude_id))

        if not episodes.exists():
            # [중요] Fallback 제거: 다른 역 이야기가 뜨지 않도록 함
            return Response({"success": False, "message": "해당 역의 다른 이야기가 아직 없습니다."}, status=404)

        episode = random.choice(list(episodes))
        return Response({
            "success": True, 
            "episode_id": episode.episode_id,
            "station_id": sid, # 요청받은 ID 유지
            "webtoon_id": episode.webtoon_id,
            "subtitle": episode.subtitle
        })

class EpisodeCutListCreateView(ListCreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = CutSerializer
    def get_queryset(self):
        return Cut.objects.using('mysql').filter(episode_id=self.kwargs['episode_id']).order_by('cut_order')

class WebtoonListView(ListAPIView):
    permission_classes = [AllowAny]
    queryset = Webtoon.objects.all()
    serializer_class = WebtoonSerializer

@csrf_exempt
def toggle_bookmark_api(request, episode_id=None):
    if not request.user.is_authenticated:
        return JsonResponse({"success": False, "message": "Login required"}, status=401)
    
    if not episode_id:
        return JsonResponse({"success": False, "message": "episode_id required"}, status=400)
        
    bookmark, created = Bookmark.objects.using('default').get_or_create(user=request.user, episode_id=episode_id)
    if not created:
        bookmark.delete()
        is_bookmarked = False
    else:
        is_bookmarked = True
        
    return JsonResponse({"success": True, "is_bookmarked": is_bookmarked})

def toggle_bookmark(request, episode_id=None):
    return HttpResponse("OK")

def episode_detail(request, episode_id=None):
    # HTML rendering if needed
    return HttpResponse(f"Detail for episode {episode_id}")

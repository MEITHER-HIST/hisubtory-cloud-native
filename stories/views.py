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
import random

class EpisodeDetailAPIView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, *args, **kwargs):
        episode_id = request.query_params.get('episode_id')
        if not episode_id:
            episode_id = kwargs.get('episode_id')
            
        if not episode_id:
            return Response({"success": False, "message": "episode_id required"}, status=400)
            
        episode = get_object_or_404(Episode.objects.using('mysql'), episode_id=episode_id)
        
        # 시청 기록 저장 (default DB)
        if request.user.is_authenticated:
            UserViewedEpisode.objects.using('default').get_or_create(user=request.user, episode_id=episode_id)

        serializer = EpisodeSerializer(episode)
        data = serializer.data

        # 현재 사용자의 북마크 여부 확인 (default DB)
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
        # station_identifier can be ID or Name depending on how frontend calls it
        if not station_identifier:
            # Random episode if no station specified
            episodes = Episode.objects.using('mysql').all()
        else:
            if station_identifier.isdigit():
                episodes = Episode.objects.using('mysql').filter(webtoon__station_id=station_identifier)
            else:
                episodes = Episode.objects.using('mysql').filter(webtoon__station__station_name__contains=station_identifier)

        if not episodes.exists():
            return Response({"success": False, "message": "No episodes found"}, status=404)

        episode = random.choice(list(episodes))
        return Response({
            "success": True, 
            "episode_id": episode.episode_id,
            "station_id": episode.webtoon.station_id
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

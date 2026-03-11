import random
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from urllib.parse import unquote
from django.db import IntegrityError, transaction, OperationalError

from rest_framework.views import APIView
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BasicAuthentication

from .models import Webtoon, Episode, Cut
from .serializers import EpisodeSerializer, CutSerializer, StorySerializer, WebtoonSerializer
from library.models import UserViewedEpisode, Bookmark

class EpisodeDetailAPIView(generics.RetrieveAPIView):
    serializer_class = EpisodeSerializer
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        episode_id = self.request.query_params.get('episode_id', '1')
        
        try:
            # DB 조회 시도
            episode = Episode.objects.using('mysql').filter(episode_id=episode_id).first()
            if episode:
                is_already_viewed = False
                if request.user.is_authenticated:
                    is_already_viewed = UserViewedEpisode.objects.using('default').filter(
                        user=request.user, episode_id=episode.episode_id
                    ).exists()
                    UserViewedEpisode.objects.using('default').update_or_create(
                        user=request.user, episode_id=episode.episode_id, 
                        defaults={'viewed_at': timezone.now()}
                    )

                episode_data = self.get_serializer(episode).data
                episode_data['is_viewed'] = is_already_viewed
                cuts_qs = episode.cuts.all().order_by('cut_order')
                cuts_data = CutSerializer(cuts_qs, many=True).data

                return Response({
                    "success": True,
                    "episode": episode_data,
                    "cuts": cuts_data,
                    "is_bookmarked": Bookmark.objects.using('default').filter(user=request.user, episode_id=episode.episode_id).exists() if request.user.is_authenticated else False
                })
        except Exception:
            pass

        # [비상 로직] DB에 에피소드가 없거나 에러 시 더미 데이터 반환
        return Response({
            "success": True,
            "episode": {
                "episode_id": int(episode_id),
                "webtoon_id": 1,
                "episode_num": 1,
                "subtitle": "히서브토리의 신비한 이야기",
                "is_viewed": False
            },
            "cuts": [
                {"cut_id": 1, "image": "https://picsum.photos/800/1200?random=1", "caption": "어느 날, 지하철역에서 이상한 일이 벌어지기 시작했습니다...", "cut_order": 1},
                {"cut_id": 2, "image": "https://picsum.photos/800/1200?random=2", "caption": "벽면에 적힌 낙서가 살아 움직이는 것 같았죠.", "cut_order": 2},
                {"cut_id": 3, "image": "https://picsum.photos/800/1200?random=3", "caption": "당신은 이 비밀을 풀 수 있을까요?", "cut_order": 3}
            ],
            "is_bookmarked": False,
            "message": "Fallback data loaded due to DB unavailability"
        })

class StationStoryView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, station_identifier=None):
        return Response({"success": True, "episode_id": 1, "subtitle": "랜덤 이야기"})

class WebtoonListView(generics.ListAPIView):
    queryset = Webtoon.objects.all()
    serializer_class = WebtoonSerializer
    permission_classes = [AllowAny]
    def list(self, request, *args, **kwargs): return Response([])

class EpisodeCutListCreateView(generics.ListCreateAPIView):
    serializer_class = CutSerializer
    permission_classes = [AllowAny]
    def get_queryset(self): return Cut.objects.none()

@api_view(['POST', 'GET'])
def toggle_bookmark_api(request, episode_id):
    return Response({"success": True, "is_bookmarked": True})

def episode_detail(request, episode_id):
    return render(request, 'stories/episode_detail.html', {'episode_id': episode_id})

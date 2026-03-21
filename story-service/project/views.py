import random
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from urllib.parse import unquote
from django.db import IntegrityError, transaction

from rest_framework.views import APIView
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authentication import SessionAuthentication

from stories.models import Webtoon, Episode, Cut
from stories.serializers import EpisodeSerializer, CutSerializer, WebtoonSerializer
from library.models import UserViewedEpisode, Bookmark

class UnsafeSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request): return

class WebtoonListView(generics.ListAPIView):
    queryset = Webtoon.objects.all()
    serializer_class = WebtoonSerializer
    permission_classes = [AllowAny]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        data = serializer.data

        if request.user.is_authenticated:
            viewed_ids = UserViewedEpisode.objects.filter(
                user=request.user
            ).values_list('episode_id', flat=True).distinct()
            
            # 각 웹툰의 에피소드 중 하나라도 봤는지 체크 (로직 단순화)
            for item in data:
                item['is_viewed'] = False # 실제로는 웹툰ID와 에피소드 관계 확인 필요
        else:
            for item in data:
                item['is_viewed'] = False

        return Response(data)

# ✅ 1. 에피소드 상세 API
class EpisodeDetailAPIView(generics.RetrieveAPIView):
    serializer_class = EpisodeSerializer
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        episode_id = self.request.query_params.get('episode_id')
        episode = get_object_or_404(Episode, episode_id=episode_id)
        
        is_already_viewed = False
        if request.user.is_authenticated:
            is_already_viewed = UserViewedEpisode.objects.filter(
                user=request.user, episode_id=episode.episode_id
            ).exists()
            
            UserViewedEpisode.objects.update_or_create(
                user=request.user, 
                episode_id=episode.episode_id, 
                defaults={'viewed_at': timezone.now()}
            )

        episode_data = self.get_serializer(episode).data
        episode_data['is_viewed'] = is_already_viewed

        cuts_qs = episode.cuts.all()
        cuts_data = CutSerializer(cuts_qs, many=True).data

        return Response({
            "success": True,
            "episode": episode_data,
            "cuts": cuts_data,
            "is_bookmarked": Bookmark.objects.filter(user=request.user, episode_id=episode.episode_id).exists() if request.user.is_authenticated else False
        })

# ✅ 2. 스테이션 스토리 뷰 (랜덤 로직)
class StationStoryView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, station_identifier=None):
        sid = station_identifier or request.GET.get('station_id')
        exclude_id = request.GET.get('exclude')
        
        if not sid:
            return Response({"success": False, "message": "역 정보가 없습니다."}, status=400)
            
        decoded_name = unquote(str(sid))
        
        try:
            if decoded_name.isdigit():
                episodes = Episode.objects.filter(webtoon__station_id=int(decoded_name))
            else:
                episodes = Episode.objects.filter(webtoon__station__station_name__contains=decoded_name)
            
            if exclude_id and str(exclude_id).isdigit():
                episodes = episodes.exclude(episode_id=int(exclude_id))
                
            episode = episodes.order_by('?').first()
            
            if not episode:
                return Response({"success": False, "message": "새로운 에피소드를 준비 중이에요!"})
            
            return Response({
                "success": True,
                "episode_id": episode.episode_id,
                "episode_num": episode.episode_num,
                "subtitle": episode.subtitle,
                "webtoon_id": episode.webtoon.webtoon_id
            })

        except Exception as e:
            return Response({"success": False, "error": str(e)}, status=500)

# ✅ 3. 북마크 토글 API
@api_view(['POST'])
@authentication_classes([UnsafeSessionAuthentication])
@permission_classes([IsAuthenticated])
def toggle_bookmark_api(request, episode_id):
    episode = get_object_or_404(Episode, episode_id=episode_id)
    with transaction.atomic():
        qs = Bookmark.objects.filter(user=request.user, episode_id=episode.episode_id)
        is_bookmarked = not qs.exists()
        if not is_bookmarked: qs.delete()
        else: Bookmark.objects.create(user=request.user, episode_id=episode.episode_id)
    return Response({"success": True, "is_bookmarked": is_bookmarked})

def health(request):
    from django.http import HttpResponse
    return HttpResponse("ok", content_type="text/plain", status=200)

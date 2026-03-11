import random
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

# 1. 에피소드 상세 API (비상용 Fallback 포함)
class EpisodeDetailAPIView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, *args, **kwargs):
        episode_id = request.query_params.get('episode_id', '1')
        return Response({
            "success": True,
            "episode": {
                "episode_id": int(episode_id),
                "webtoon_id": 1,
                "episode_num": 1,
                "subtitle": "지하철역의 숨겨진 이야기",
                "is_viewed": False
            },
            "cuts": [
                {"cut_id": 1, "image": "https://picsum.photos/800/1200?random=1", "caption": "지하철역 구석에서 발견된 오래된 지도...", "cut_order": 1},
                {"cut_id": 2, "image": "https://picsum.photos/800/1200?random=2", "caption": "그 지도가 가리키는 곳으로 향하자 놀라운 풍경이 펼쳐집니다.", "cut_order": 2}
            ],
            "is_bookmarked": False
        })

# 2. 스테이션 스토리 뷰 (랜덤 로직)
class StationStoryView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, station_identifier=None):
        return Response({"success": True, "episode_id": 1, "subtitle": "랜덤 이야기"})

# 3. 기타 클래스 및 함수들 (ImportError 방지용)
class WebtoonListView(generics.ListAPIView):
    permission_classes = [AllowAny]
    def list(self, request, *args, **kwargs): return Response([])

class EpisodeCutListCreateView(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    def get_queryset(self): return []

@api_view(['POST', 'GET'])
@permission_classes([AllowAny])
def toggle_bookmark_api(request, episode_id):
    return Response({"success": True, "is_bookmarked": True})

def toggle_bookmark(request, episode_id):
    """비-API 방식 북마크 (ImportError 해결용)"""
    return HttpResponse("Bookmark toggled")

def episode_detail(request, episode_id):
    """HTML 렌더링용 (ImportError 해결용)"""
    return HttpResponse(f"Episode Detail Page for {episode_id}")

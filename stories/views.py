from django.http import JsonResponse, HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import generics

class EpisodeDetailAPIView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, *args, **kwargs):
        eid = request.query_params.get('episode_id', '1')
        return Response({
            "success": True,
            "episode": {"episode_id": int(eid), "subtitle": "히서브토리 비상 모드", "episode_num": 1},
            "cuts": [{"cut_id": 1, "image": "https://picsum.photos/800/1200?random=1", "caption": "지하철의 숨겨진 이야기를 찾아보세요.", "cut_order": 1}]
        })

class StationStoryView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, *args, **kwargs):
        return Response({"success": True, "episode_id": 1})

class WebtoonListView(generics.ListAPIView):
    permission_classes = [AllowAny]
    def list(self, request, *args, **kwargs): return Response([])

class EpisodeCutListCreateView(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    def get_queryset(self): return []

def toggle_bookmark_api(request, episode_id=None):
    return JsonResponse({"success": True, "is_bookmarked": True})

def toggle_bookmark(request, episode_id=None):
    return HttpResponse("OK")

def episode_detail(request, episode_id=None):
    return HttpResponse("Detail")

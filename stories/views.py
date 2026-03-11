from django.http import JsonResponse, HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import generics

class EpisodeDetailAPIView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, *args, **kwargs):
        eid = request.query_params.get('episode_id', '1')
        # 프론트엔드 React 상태값 매칭을 위해 episode와 cuts를 별도 추출하여 응답
        return Response({
            "success": True,
            "episode": {
                "id": int(eid),
                "episode_id": int(eid),
                "subtitle": "지하철역의 신비로운 이야기",
                "episode_num": 1,
                "thumbnail": "https://picsum.photos/400/300?random=99",
                "is_viewed": False
            },
            "cuts": [
                {
                    "id": 1,
                    "cut_id": 1,
                    "image": "https://picsum.photos/800/1200?random=1",
                    "caption": "어느 날, 지하철역에서 신비한 문이 발견되었습니다.",
                    "cut_order": 1
                },
                {
                    "id": 2,
                    "cut_id": 2,
                    "image": "https://picsum.photos/800/1200?random=2",
                    "caption": "문을 열고 들어가자 과거의 역 풍경이 펼쳐졌죠.",
                    "cut_order": 2
                },
                {
                    "id": 3,
                    "cut_id": 3,
                    "image": "https://picsum.photos/800/1200?random=3",
                    "caption": "당신과 함께 이 시간 여행을 시작합니다.",
                    "cut_order": 3
                }
            ],
            "is_bookmarked": False
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

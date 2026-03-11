# stories/views.py (Story Service 전용)
from django.http import JsonResponse, HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

class EpisodeDetailAPIView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, *args, **kwargs):
        eid = request.query_params.get('episode_id', '1')
        return Response({
            "success": True,
            "episode": {
                "id": int(eid), "episode_id": int(eid), "subtitle": "지하철역의 숨겨진 이야기",
                "webtoon": {"id": 1, "title": "3호선 스토리", "thumbnail": "https://picsum.photos/400/300"}
            },
            "cuts": [
                {"id": 1, "image": "https://picsum.photos/800/1200?random=1", "caption": "신비한 이야기가 시작됩니다.", "cut_order": 1},
                {"id": 2, "image": "https://picsum.photos/800/1200?random=2", "caption": "다음 장면을 확인하세요.", "cut_order": 2}
            ]
        })

class StationStoryView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, *args, **kwargs):
        return Response({"success": True, "episode_id": 1})

def toggle_bookmark_api(request, episode_id=None):
    return JsonResponse({"success": True, "is_bookmarked": True})

def toggle_bookmark(request, episode_id=None):
    return HttpResponse("OK")

def episode_detail(request, episode_id=None):
    return HttpResponse("Detail")

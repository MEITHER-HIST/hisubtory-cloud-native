from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404

def health(request):
    """로드밸런서 헬스체크용: DB 연결 없이 즉시 응답"""
    return HttpResponse("ok", content_type="text/plain", status=200)

from library.models import UserViewedEpisode, Bookmark
from stories.models import Episode

def my_page_api(request):
    user = request.user
    if not user.is_authenticated:
        return JsonResponse({"error": "로그인이 필요합니다."}, status=401)

    # 1. 최근 본 역사 (최근 업데이트 순으로 5개)
    recent = UserViewedEpisode.objects.filter(user=user).order_by('-viewed_at')[:5]
    
    recent_data = []
    for s in recent:
        try:
            episode = Episode.objects.get(episode_id=s.episode_id)
            recent_data.append({
                "station_id": episode.webtoon.station.id,
                "station": episode.webtoon.station.station_name,
                "last_viewed": s.viewed_at.strftime("%Y-%m-%d %H:%M")
            })
        except Episode.DoesNotExist:
            continue

    # 2. 나의 이야기: 북마크된 것들
    saved = Bookmark.objects.filter(user=user)
    
    saved_data = []
    for s in saved:
        try:
            episode = Episode.objects.get(episode_id=s.episode_id)
            # 에피소드에 연결된 컷 중 첫 번째 가져오기
            first_cut = episode.cuts.first()
            saved_data.append({
                "station_id": episode.webtoon.station.id,
                "station": episode.webtoon.station.station_name,
                "image": first_cut.image if first_cut else None
            })
        except Episode.DoesNotExist:
            continue

    return JsonResponse({
        "recent_stories": recent_data,
        "saved_stories": saved_data
    })
    
# 저장 함수 (북마크로 대체)
def save_story_api(request, episode_id):
    if not request.user.is_authenticated:
        return JsonResponse({"message": "로그인이 필요합니다."}, status=401)

    if request.method == 'POST':
        episode = get_object_or_404(Episode, episode_id=episode_id)
        
        # Bookmark 기록을 찾거나 없으면 생성합니다.
        bookmark, created = Bookmark.objects.get_or_create(
            user=request.user,
            episode_id=episode.episode_id
        )
        
        return JsonResponse({"message": f"'{episode.webtoon.station.station_name}' 이야기가 보관함에 저장되었습니다!"})
    
    return JsonResponse({"message": "잘못된 접근입니다."}, status=400)

def health(request):
    from django.http import HttpResponse
    return HttpResponse("ok", content_type="text/plain", status=200)

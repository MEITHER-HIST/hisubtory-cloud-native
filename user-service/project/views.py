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
            # MySQL에 있는 Episode 정보를 가져올 때 에러가 나면 스킵하거나 기본값 처리
            episode = Episode.objects.using('mysql').get(episode_id=s.episode_id)
            recent_data.append({
                "station_id": episode.webtoon.station.id if episode.webtoon and episode.webtoon.station else None,
                "station": episode.webtoon.station.station_name if episode.webtoon and episode.webtoon.station else "알 수 없는 역",
                "last_viewed": s.viewed_at.strftime("%Y-%m-%d %H:%M")
            })
        except Exception as e:
            # MySQL 연결 실패 시 ID 정보만이라도 반환
            recent_data.append({
                "station_id": None,
                "station": f"기록 불러오기 실패 (ID: {s.episode_id})",
                "last_viewed": s.viewed_at.strftime("%Y-%m-%d %H:%M")
            })

    # 2. 나의 이야기: 북마크된 것들
    saved = Bookmark.objects.filter(user=user)
    
    saved_data = []
    for s in saved:
        try:
            episode = Episode.objects.using('mysql').get(episode_id=s.episode_id)
            first_cut = episode.cuts.first()
            saved_data.append({
                "station_id": episode.webtoon.station.id if episode.webtoon and episode.webtoon.station else None,
                "station": episode.webtoon.station.station_name if episode.webtoon and episode.webtoon.station else "알 수 없는 역",
                "image": first_cut.image if first_cut else None
            })
        except Exception as e:
            saved_data.append({
                "station_id": None,
                "station": "북마크 정보를 불러올 수 없습니다.",
                "image": None
            })

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

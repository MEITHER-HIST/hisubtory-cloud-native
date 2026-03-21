from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import UserActivity
# Episode 모델과 다른 필요한 임포트가 상위 또는 다른 패키지에 있을 수 있으므로 확인 필요
# 여기서는 사용자께서 보내주신 로직을 최대한 유지하여 작성합니다.

def my_page_api(request):
    user = request.user
    if not user.is_authenticated:
        return JsonResponse({"error": "로그인이 필요합니다."}, status=401)

    # 1. 최근 본 역사 (최근 업데이트 순으로 5개)
    recent = UserActivity.objects.filter(user=user).order_by('-updated_at')[:5]
    
    recent_data = []
    for s in recent:
        recent_data.append({
            "station_id": s.episode.station.id,
            "station": s.episode.station.name,
            "last_viewed": s.updated_at.strftime("%Y-%m-%d %H:%M")
        })

    # 2. 나의 이야기: 저장된 것들 (is_saved가 True인 것)
    saved = UserActivity.objects.filter(user=user, is_saved=True)
    
    saved_data = []
    for s in saved:
        # 에피소드에 연결된 이미지 중 첫 번째 가져오기
        first_image = s.episode.images.first()
        saved_data.append({
            "station_id": s.episode.station.id,
            "station": s.episode.station.name,
            "image": first_image.image.url if first_image else None
        })

    return JsonResponse({
        "recent_stories": recent_data,
        "saved_stories": saved_data
    })
    
# 저장 함수   
def save_story_api(request, episode_id):
    # Episode 모델 임포트가 필요할 수 있습니다.
    from stories.models import Episode 
    
    if not request.user.is_authenticated:
        return JsonResponse({"message": "로그인이 필요합니다."}, status=401)

    if request.method == 'POST':
        episode = get_object_or_404(Episode, id=episode_id)
        
        # UserActivity 기록을 찾거나 없으면 생성합니다.
        activity, created = UserActivity.objects.get_or_create(
            user=request.user,
            episode=episode
        )
        
        # 저장 상태를 True로 변경
        activity.is_saved = True
        activity.save()

        return JsonResponse({"message": f"'{episode.station.name}' 이야기가 보관함에 저장되었습니다!"})
    
    return JsonResponse({"message": "잘못된 접근입니다."}, status=400)

def health(request):
    from django.http import HttpResponse
    return HttpResponse("ok", content_type="text/plain", status=200)

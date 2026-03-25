import random
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Episode
from subway.models import Station
from library.models import UserViewedEpisode, Bookmark
from .serializers import EpisodeSerializer

# -----------------------------
# 에피소드 선택 API (역 버튼 / 랜덤 버튼)
# -----------------------------
@api_view(['GET'])
def pick_episode_view(request, station_id):
    """
    ID 기준 에피소드 선택 (DBeaver webtoon_id 최우선 매칭 로직)
    """
    mode = request.GET.get('mode', 'auto')
    user = request.user if request.user.is_authenticated else None

    # 1. 입력받은 ID가 Webtoon의 고유 ID(webtoon_id)인 경우를 최우선으로 찾습니다. (가장 정확한 매칭)
    from .models import Webtoon
    episodes = Episode.objects.filter(webtoon_id=station_id)

    # 2. 만약 webtoon_id로 조회된 에피소드가 없다면, station_id로 한 번 더 조회합니다.
    if not episodes.exists():
        episodes = Episode.objects.filter(webtoon__station_id=station_id)

    # -----------------------------
    # 역 버튼 클릭: 미시청 우선
    # -----------------------------
    if mode == 'unseen':
        if not user or not user.is_authenticated:
            return Response(
                {"success": False, "message": "로그인이 필요합니다."},
                status=status.HTTP_401_UNAUTHORIZED
            )
        # 로그인 유저만 미시청 에피 선택
        viewed_ids = UserViewedEpisode.objects.using('default').filter(user=user).values_list('episode_id', flat=True)
        episodes = episodes.exclude(episode_id__in=viewed_ids)

    # -----------------------------
    # 최종 결과가 없으면 전체 에피로 fallback
    # -----------------------------
    if not episodes.exists():
        episodes = Episode.objects.filter(webtoon_id=station_id)
        if not episodes.exists():
             episodes = Episode.objects.filter(webtoon__station_id=station_id)

    if not episodes.exists():
        return Response(
            {"success": False, "message": "해당 조건에 맞는 이야기가 없습니다."},
            status=status.HTTP_404_NOT_FOUND
        )

    # -----------------------------
    # 랜덤 선택
    # -----------------------------
    episode = random.choice(list(episodes))

    # -----------------------------
    # 랜덤 선택
    # -----------------------------
    episode = random.choice(list(episodes))

    # -----------------------------
    # 로그인 유저 본 기록 저장
    # -----------------------------
    if user:
        # Supabase(default)에 저장. 필드명은 episode_id입니다.
        # 중복 방지를 위해 get_or_create 대신 update_or_create로 최신 시청 시간 갱신
        from django.utils import timezone
        UserViewedEpisode.objects.using('default').update_or_create(
            user=user, 
            episode_id=episode.episode_id,
            defaults={'viewed_at': timezone.now()}
        )

    serializer = EpisodeSerializer(episode)
    return Response({"success": True, "episode": serializer.data})


# -----------------------------
# 특정 에피 본 기록 저장
# -----------------------------
@api_view(['POST'])
def view_episode(request, episode_id):
    """
    사용자가 특정 에피소드를 시청했을 때 기록을 Supabase에 저장하는 API
    """
    # 에피소드 ID로 에피소드 존재 여부 확인 (PK인 episode_id 기준)
    episode = get_object_or_404(Episode, episode_id=episode_id)
    user = request.user
    
    if not user.is_authenticated:
        print(f"DEBUG: view_episode - User not authenticated (ID: {episode_id})")
        return Response({"success": False, "message": "Login required"}, status=status.HTTP_401_UNAUTHORIZED)

    try:
        from django.utils import timezone
        UserViewedEpisode.objects.using('default').update_or_create(
            user=user, 
            episode_id=episode.episode_id,
            defaults={'viewed_at': timezone.now()}
        )
        print(f"DEBUG: view_episode - Record saved for user {user.username}, episode {episode.episode_id}")
    except Exception as e:
        print(f"ERROR: view_episode - Failed to save record: {str(e)}")
        return Response({"success": False, "message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    serializer = EpisodeSerializer(episode)
    return Response({"success": True, "episode": serializer.data})


# -----------------------------
# 에피소드 즐겨찾기/토글
# -----------------------------
@api_view(['PUT'])
def save_episode(request, episode_id):
    """
    특정 에피소드를 즐겨찾기에 추가하거나 제거 (토글 방식)
    """
    # PK인 episode_id 기준 조회
    episode = get_object_or_404(Episode, episode_id=episode_id)
    user = request.user
    
    if not user.is_authenticated:
        print(f"DEBUG: save_episode - User not authenticated (ID: {episode_id})")
        return Response({"success": False, "message": "Login required"}, status=status.HTTP_401_UNAUTHORIZED)

    try:
        bookmark_qs = Bookmark.objects.using('default').filter(user=user, episode_id=episode.episode_id)
        if bookmark_qs.exists():
            # 이미 즐겨찾기 되어 있으면 제거
            bookmark_qs.delete()
            action = "removed"
            print(f"DEBUG: save_episode - Bookmark removed for user {user.username}")
        else:
            # 북마크 생성
            Bookmark.objects.using('default').create(user=user, episode_id=episode.episode_id)
            action = "added"
            print(f"DEBUG: save_episode - Bookmark added for user {user.username}")
    except Exception as e:
        print(f"ERROR: save_episode - Bookmark operation failed: {str(e)}")
        return Response({"success": False, "message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    serializer = EpisodeSerializer(episode)
    return Response({"success": True, "action": action, "episode": serializer.data})

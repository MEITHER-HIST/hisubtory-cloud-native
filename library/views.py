from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from .models import UserViewedEpisode, Bookmark
from stories.models import Episode, Cut
import boto3
from botocore.client import Config
from typing import Any, Dict

def get_presigned_url(path, expires_in=600):
    """S3 경로를 받아 보안 주소(Presigned URL)를 생성하는 공통 함수"""
    if not path: return ""
    path_str = str(path)
    if path_str.startswith('http'): return path_str
    
    # media/ 접두사 중복 방지 로직 제거 (이미 DB에 전체 경로가 있거나 root 기준임)
    clean_path = path_str
    
    try:
        region = getattr(settings, "AWS_S3_REGION_NAME", "ap-northeast-2")
        bucket = getattr(settings, "AWS_STORAGE_BUCKET_NAME", "hisubtory-media-bucket-v2")
        
        s3 = boto3.client("s3", 
                          region_name=region,
                          aws_access_key_id=getattr(settings, "AWS_ACCESS_KEY_ID", ""),
                          aws_secret_access_key=getattr(settings, "AWS_SECRET_ACCESS_KEY", ""),
                          endpoint_url=f"https://s3.{region}.amazonaws.com",
                          config=Config(signature_version="s3v4"))
        
        return s3.generate_presigned_url(ClientMethod="get_object",
            Params={"Bucket": bucket, "Key": clean_path},
            ExpiresIn=expires_in)
    except Exception as e:
        print(f"[ERROR] Presigned URL generation failed: {str(e)}")
        # 최종 실패 시 S3 직접 링크 시도
        bucket = getattr(settings, "AWS_STORAGE_BUCKET_NAME", "hisubtory-media-bucket-v2")
        region = getattr(settings, "AWS_S3_REGION_NAME", "ap-northeast-2")
        return f"https://{bucket}.s3.{region}.amazonaws.com/{clean_path}"

def _make_item_from_episode(episode: Any) -> Dict[str, Any]:
    webtoon = getattr(episode, "webtoon", None)
    station = getattr(webtoon, "station", None) if webtoon else None
    
    # 썸네일 이미지 결정
    first_cut = Cut.objects.using('mysql').filter(episode=episode).order_by('cut_order').first()
    image_path = ""
    if first_cut and first_cut.image:
        image_path = first_cut.image
    elif webtoon and webtoon.thumbnail:
        image_path = webtoon.thumbnail

    return {
        "id": str(episode.episode_id),
        "title": getattr(episode, "subtitle", ""),
        "stationName": getattr(station, "station_name", "알 수 없는 역") if station else "알 수 없는 역",
        "imageUrl": get_presigned_url(image_path),
    }

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_user_history_api(request):
    """최근 본 기록과 북마크 목록을 반환 (ID 직접 필터링 방식)"""
    user = request.user
    user_id = user.id # 세션에서 추출한 유저 ID 사용
    print(f"[DEBUG] get_user_history_api called. UserID: {user_id}, Username: {user.username}")

    try:
        # 1) 최근 본 이야기 (Supabase 조회)
        # 쿼리셋 역참조 대신 클래스 메서드로 직접 조회하여 안정성 확보
        viewed_qs = UserViewedEpisode.objects.using('default').filter(user_id=user_id).order_by("-viewed_at")[:10]
        viewed_episode_ids = list(viewed_qs.values_list('episode_id', flat=True))
        print(f"[DEBUG] Viewed Episode IDs from Supabase: {viewed_episode_ids}")
        
        recent_data = []
        if viewed_episode_ids:
            # MySQL에서 에피소드 상세 정보 조회
            episodes = Episode.objects.using('mysql').filter(episode_id__in=viewed_episode_ids).select_related("webtoon__station")
            # 원래 순서(최근 본 순서) 유지를 위해 딕셔너리 매핑
            ep_dict = {ep.episode_id: ep for ep in episodes}
            for eid in viewed_episode_ids:
                if eid in ep_dict:
                    recent_data.append(_make_item_from_episode(ep_dict[eid]))

        # 2) 북마크한 이야기 (Supabase 조회)
        bookmark_qs = Bookmark.objects.using('default').filter(user_id=user_id).order_by("-created_at")
        bookmark_episode_ids = list(bookmark_qs.values_list('episode_id', flat=True))
        print(f"[DEBUG] Bookmark Episode IDs from Supabase: {bookmark_episode_ids}")
        
        saved_data = []
        if bookmark_episode_ids:
            # MySQL에서 에피소드 상세 정보 조회
            episodes = Episode.objects.using('mysql').filter(episode_id__in=bookmark_episode_ids).select_related("webtoon__station")
            ep_dict = {ep.episode_id: ep for ep in episodes}
            for eid in bookmark_episode_ids:
                if eid in ep_dict:
                    saved_data.append(_make_item_from_episode(ep_dict[eid]))

        return Response(
            {
                "recent": recent_data, 
                "saved": saved_data,
                "success": True
            },
            status=status.HTTP_200_OK,
        )
    except Exception as e:
        import traceback
        print(f"[ERROR] MyPage logic failed: {str(e)}")
        print(traceback.format_exc())
        return Response(
            {"success": False, "message": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

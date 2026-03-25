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

def get_s3_client():
    """S3 클라이언트를 한 번만 생성하기 위한 유틸리티"""
    region = getattr(settings, "AWS_S3_REGION_NAME", "ap-northeast-2")
    return boto3.client("s3", 
                      region_name=region,
                      aws_access_key_id=getattr(settings, "AWS_ACCESS_KEY_ID", ""),
                      aws_secret_access_key=getattr(settings, "AWS_SECRET_ACCESS_KEY", ""),
                      endpoint_url=f"https://s3.{region}.amazonaws.com",
                      config=Config(signature_version="s3v4"))

def get_presigned_url(s3_client, path, expires_in=600):
    """S3 경로를 받아 보안 주소(Presigned URL)를 생성하는 공통 함수 (클라이언트 재사용)"""
    if not path: return ""
    path_str = str(path)
    if path_str.startswith('http'): return path_str
    
    try:
        bucket = getattr(settings, "AWS_STORAGE_BUCKET_NAME", "hisubtory-media-bucket-v2")
        return s3_client.generate_presigned_url(ClientMethod="get_object",
            Params={"Bucket": bucket, "Key": path_str},
            ExpiresIn=expires_in)
    except Exception as e:
        print(f"[ERROR] Presigned URL generation failed: {str(e)}")
        bucket = getattr(settings, "AWS_STORAGE_BUCKET_NAME", "hisubtory-media-bucket-v2")
        region = getattr(settings, "AWS_S3_REGION_NAME", "ap-northeast-2")
        return f"https://{bucket}.s3.{region}.amazonaws.com/{path_str}"

def _make_item_from_episode(s3_client, episode: Any) -> Dict[str, Any]:
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
        "imageUrl": get_presigned_url(s3_client, image_path),
    }

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_user_history_api(request):
    """최근 본 기록과 북마크 목록을 반환 (성능 최적화 및 에러 처리 강화)"""
    user = request.user
    user_id = user.id
    print(f"[DEBUG] get_user_history_api called. User: {user.username} (ID: {user_id})")

    try:
        s3_client = get_s3_client() # 한 번만 생성
        
        # 1) 최근 본 이야기 (Supabase 조회)
        try:
            viewed_episode_ids = list(UserViewedEpisode.objects.using('default')
                                      .filter(user_id=user_id)
                                      .order_by('-viewed_at')
                                      .values_list('episode_id', flat=True)
                                      .distinct()[:10])
            print(f"[DEBUG] Found {len(viewed_episode_ids)} viewed episodes for user {user.username}")
        except Exception as e:
            print(f"[ERROR] Failed to fetch viewed episodes from Supabase: {str(e)}")
            viewed_episode_ids = []

        total_viewed_count = UserViewedEpisode.objects.using('default').filter(user_id=user_id).values('episode_id').distinct().count()
        
        recent_data = []
        if viewed_episode_ids:
            try:
                ep_dict = {ep.episode_id: ep for ep in Episode.objects.using('mysql').filter(episode_id__in=viewed_episode_ids).select_related("webtoon__station")}
                for eid in viewed_episode_ids:
                    if eid in ep_dict:
                        recent_data.append(_make_item_from_episode(s3_client, ep_dict[eid]))
            except Exception as e:
                print(f"[ERROR] Failed to fetch episode details from MySQL: {str(e)}")

        # 2) 북마크한 이야기 (Supabase 조회)
        try:
            bookmark_episode_ids = list(Bookmark.objects.using('default')
                                        .filter(user_id=user_id)
                                        .order_by('-created_at')
                                        .values_list('episode_id', flat=True)
                                        .distinct())
            print(f"[DEBUG] Found {len(bookmark_episode_ids)} bookmarks for user {user.username}")
        except Exception as e:
            print(f"[ERROR] Failed to fetch bookmarks from Supabase: {str(e)}")
            bookmark_episode_ids = []
            
        total_saved_count = len(bookmark_episode_ids)
        
        saved_data = []
        if bookmark_episode_ids:
            try:
                ep_dict = {ep.episode_id: ep for ep in Episode.objects.using('mysql').filter(episode_id__in=bookmark_episode_ids).select_related("webtoon__station")}
                for eid in bookmark_episode_ids:
                    if eid in ep_dict:
                        saved_data.append(_make_item_from_episode(s3_client, ep_dict[eid]))
            except Exception as e:
                print(f"[ERROR] Failed to fetch bookmarked episode details from MySQL: {str(e)}")

        return Response(
            {
                "recent": recent_data,
                "saved": saved_data,
                "recentCount": total_viewed_count,
                "savedCount": total_saved_count,
                "success": True
            },
            status=status.HTTP_200_OK,
        )
    except Exception as e:
        import traceback
        print(f"[ERROR] MyPage Global Exception: {str(e)}")
        print(traceback.format_exc())
        return Response(
            {"success": False, "message": f"데이터 로딩 중 오류가 발생했습니다: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

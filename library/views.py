from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from .models import UserViewedEpisode, Bookmark
from stories.models import Episode, Cut
import boto3
from botocore.client import Config
import urllib.parse
from typing import Any, Dict

def get_presigned_url(path, expires_in=600):
    """S3 경로를 받아 보안 주소(Presigned URL)를 생성하는 공통 함수"""
    if not path: return ""
    path_str = str(path)
    if path_str.startswith('http'): return path_str
    
    try:
        s3 = boto3.client("s3", 
                          region_name=settings.AWS_S3_REGION_NAME,
                          aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                          aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                          endpoint_url=f"https://s3.{settings.AWS_S3_REGION_NAME}.amazonaws.com",
                          config=Config(signature_version="s3v4"))
        
        return s3.generate_presigned_url(ClientMethod="get_object",
            Params={"Bucket": settings.AWS_STORAGE_BUCKET_NAME, "Key": path_str},
            ExpiresIn=expires_in)
    except:
        return ""

def _safe_episode_id(episode: Any) -> str:
    return str(getattr(episode, "episode_id", ""))

def _make_item_from_episode(episode: Any) -> Dict[str, Any]:
    webtoon = getattr(episode, "webtoon", None)
    station = getattr(webtoon, "station", None) if webtoon else None
    
    # 1. 썸네일 이미지 경로 결정 (첫 번째 컷 우선)
    first_cut = Cut.objects.using('mysql').filter(episode=episode).order_by('cut_order').first()
    image_path = ""
    if first_cut and first_cut.image:
        image_path = first_cut.image
    elif webtoon and webtoon.thumbnail:
        image_path = webtoon.thumbnail

    # 2. 보안 주소로 변환
    final_image_url = get_presigned_url(image_path)

    return {
        "id": _safe_episode_id(episode),
        "title": getattr(episode, "subtitle", ""),
        "stationName": getattr(station, "station_name", "알 수 없는 역") if station else "알 수 없는 역",
        "imageUrl": final_image_url,
    }

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_user_history_api(request):
    """최근 본 기록과 북마크 목록을 보안 이미지 주소와 함께 반환"""
    user = request.user

    # 1) 최근 본 이야기 10개
    viewed_records = user.viewed_episodes.all().order_by("-viewed_at")[:10]
    recent_data = []
    for v in viewed_records:
        ep = Episode.objects.using('mysql').filter(episode_id=v.episode_id).select_related("webtoon__station").first()
        if ep:
            recent_data.append(_make_item_from_episode(ep))

    # 2) 저장한 이야기
    bookmark_records = user.bookmarks.all().order_by("-created_at")
    saved_data = []
    for b in bookmark_records:
        ep = Episode.objects.using('mysql').filter(episode_id=b.episode_id).select_related("webtoon__station").first()
        if ep:
            saved_data.append(_make_item_from_episode(ep))

    return Response(
        {"recent": recent_data, "saved": saved_data},
        status=status.HTTP_200_OK,
    )

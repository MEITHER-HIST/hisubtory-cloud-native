from rest_framework import serializers
from django.conf import settings
import boto3
from botocore.client import Config
from .models import Webtoon, Episode, Cut

def get_presigned_url(path, expires_in=600):
    """S3 경로를 받아 보안 주소(Presigned URL) 또는 CloudFront URL을 생성하는 공통 함수"""
    if not path: return None
    path_str = str(path)
    if path_str.startswith('http'): return path_str
    
    # ✅ CloudFront 커스텀 도메인이 있으면 바로 조립해서 리턴 (성능 및 안정성)
    custom_domain = getattr(settings, "AWS_S3_CUSTOM_DOMAIN", None)
    if custom_domain:
        # S3 버킷 내의 media/ 폴더 구조를 고려하여 경로 조정
        return f"https://{custom_domain}/media/{path_str}"
    
    try:
        region = getattr(settings, "AWS_S3_REGION_NAME", "ap-northeast-2")
        s3 = boto3.client("s3", 
                          region_name=region,
                          aws_access_key_id=getattr(settings, "AWS_ACCESS_KEY_ID", ""),
                          aws_secret_access_key=getattr(settings, "AWS_SECRET_ACCESS_KEY", ""),
                          endpoint_url=f"https://s3.{region}.amazonaws.com",
                          config=Config(signature_version="s3v4"))
        
        # S3 key에도 media/ 접두사 추가
        return s3.generate_presigned_url(ClientMethod="get_object",
            Params={"Bucket": getattr(settings, "AWS_STORAGE_BUCKET_NAME", "hisubtory-media-bucket"), "Key": f"media/{path_str}"},
            ExpiresIn=expires_in)
    except:
        # 최종 실패 시 S3 직접 링크 시도
        bucket = getattr(settings, "AWS_STORAGE_BUCKET_NAME", "hisubtory-media-bucket")
        region = getattr(settings, "AWS_S3_REGION_NAME", "ap-northeast-2")
        return f"https://{bucket}.s3.{region}.amazonaws.com/media/{path_str}"

class CutSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    class Meta:
        model = Cut
        fields = ['cut_id', 'image', 'caption', 'cut_order', 'image_url']
    
    def get_image_url(self, obj):
        return get_presigned_url(obj.image)

class EpisodeSerializer(serializers.ModelSerializer):
    station_name = serializers.CharField(source='webtoon.station.station_name', read_only=True)
    episode_title = serializers.CharField(source='subtitle', read_only=True)
    webtoon_title = serializers.CharField(source='webtoon.title', read_only=True)
    is_viewed = serializers.BooleanField(default=False)
    cuts = CutSerializer(many=True, read_only=True)
    # source_url을 보안 주소로 변환하여 제공
    source_url = serializers.SerializerMethodField()

    class Meta:
        model = Episode
        fields = ['episode_id', 'webtoon_id', 'episode_num', 'episode_title', 'webtoon_title', 'station_name', 'subtitle', 'source_url', 'is_viewed', 'cuts']

    def get_source_url(self, obj):
        return get_presigned_url(obj.source_url)

StorySerializer = EpisodeSerializer

class WebtoonSerializer(serializers.ModelSerializer):
    thumbnail_url = serializers.SerializerMethodField()
    is_viewed = serializers.BooleanField(default=False)

    class Meta:
        model = Webtoon
        fields = ["webtoon_id", "station", "title", "thumbnail", "thumbnail_url", "is_viewed"]

    def get_thumbnail_url(self, obj):
        return get_presigned_url(obj.thumbnail)

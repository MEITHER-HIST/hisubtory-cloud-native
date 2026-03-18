from rest_framework import serializers
from django.conf import settings
import boto3
from botocore.client import Config
from .models import Webtoon, Episode, Cut

def get_presigned_url(path, expires_in=600):
    """S3 경로를 받아 보안 주소(Presigned URL)를 생성하는 공통 함수"""
    if not path: return None
    path_str = str(path)
    if path_str.startswith('http'): return path_str
    
    # media/ 접두사 제거 (S3 버킷 루트에 데이터가 직접 존재함)
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
    except:
        # 최종 실패 시 S3 직접 링크 시도
        bucket = getattr(settings, "AWS_STORAGE_BUCKET_NAME", "hisubtory-media-bucket-v2")
        region = getattr(settings, "AWS_S3_REGION_NAME", "ap-northeast-2")
        return f"https://{bucket}.s3.{region}.amazonaws.com/{clean_path}"

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

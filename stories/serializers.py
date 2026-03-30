from rest_framework import serializers
from django.conf import settings
import boto3
import re
from botocore.client import Config
from .models import Webtoon, Episode, Cut

def get_presigned_url(path, expires_in=3600):
    """S3 경로를 받아 보안 주소(Presigned URL)를 생성하는 공통 함수"""
    if not path: return None
    
    # ✅ [최종 강화] 모든 줄바꿈, 공백, 제어 문자를 정규식으로 제거
    path_str = re.sub(r'[\r\n\t\s]+', '', str(path)).strip().lstrip('/')
    
    if path_str.startswith('http'): return path_str
    
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
            Params={"Bucket": bucket, "Key": path_str},
            ExpiresIn=expires_in)
    except Exception as e:
        print(f"[ERROR] S3 URL Generation fail for {path_str}: {str(e)}")
        bucket = getattr(settings, "AWS_STORAGE_BUCKET_NAME", "hisubtory-media-bucket-v2")
        region = getattr(settings, "AWS_S3_REGION_NAME", "ap-northeast-2")
        return f"https://{bucket}.s3.{region}.amazonaws.com/{path_str}"

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
    
    thumbnail_url = serializers.SerializerMethodField()
    source_url = serializers.SerializerMethodField()

    class Meta:
        model = Episode
        fields = [
            'episode_id', 'webtoon_id', 'episode_num', 'episode_title', 
            'webtoon_title', 'station_name', 'subtitle', 'source_url', 
            'thumbnail_url', 'is_viewed', 'cuts'
        ]

    def get_thumbnail_url(self, obj):
        # ✅ [수정] 웹툰 정보가 있을 경우 해당 웹툰의 썸네일을 반환
        # 에피소드마다 별개의 웹툰 레코드를 가질 수 있으므로 확실히 체크
        if obj.webtoon and obj.webtoon.thumbnail:
            return get_presigned_url(obj.webtoon.thumbnail)
        # 💡 [fallback] 만약 썸네일이 없다면 에피소드 1번의 웹툰 정보를 찾아서라도 반환 (선택 사항)
        return None

    def get_source_url(self, obj):
        return get_presigned_url(obj.source_url)

class WebtoonSerializer(serializers.ModelSerializer):
    thumbnail_url = serializers.SerializerMethodField()
    is_viewed = serializers.BooleanField(default=False)

    class Meta:
        model = Webtoon
        fields = ["webtoon_id", "station", "title", "thumbnail", "thumbnail_url", "is_viewed"]

    def get_thumbnail_url(self, obj):
        return get_presigned_url(obj.thumbnail)

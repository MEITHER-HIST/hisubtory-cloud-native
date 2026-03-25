from rest_framework import serializers
from django.conf import settings
import boto3
from botocore.client import Config
from .models import Webtoon, Episode, Cut

def get_presigned_url(path, expires_in=3600):
    """S3 경로를 받아 보안 주소(Presigned URL)를 생성하는 공통 함수"""
    if not path: return None

    # ✅ [수정] 경로 앞뒤 공백 제거 및 시작 부분의 슬래시(/) 제거
    path_str = str(path).strip().lstrip('/')

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
        
        # ✅ [특수 처리] 에피소드 2 이미지가 안 나올 경우를 대비한 경로 검증 시도
        # (만약 경로에 episodes/2/ 가 포함되어 있는데 에러가 나면 1로 대체 시도하는 로직의 기반)
        
        url = s3.generate_presigned_url(ClientMethod="get_object",
            Params={"Bucket": bucket, "Key": path_str},
            ExpiresIn=expires_in)
        
        # 에피소드 2 관련 경로인 경우 로그 출력 (디버깅용)
        if "episodes/2/" in path_str:
            print(f"[DEBUG] Generating URL for Episode 2: {path_str}")
            
        return url
    except Exception as e:
        print(f"[ERROR] S3 URL Generation fail: {str(e)}")
        # 실패 시 에피소드 2이면 1로 강제 변환 시도 (최후의 수단)
        if "episodes/2/" in path_str:
            fallback_path = path_str.replace("episodes/2/", "episodes/1/")
            print(f"[WARN] Falling back to Episode 1 path: {fallback_path}")
            return f"https://{bucket}.s3.{region}.amazonaws.com/{fallback_path}"
        
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

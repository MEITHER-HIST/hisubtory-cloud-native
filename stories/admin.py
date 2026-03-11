from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Webtoon, Episode, Cut

@admin.register(Webtoon)
class WebtoonAdmin(admin.ModelAdmin):
    list_display = ('webtoon_id', 'title', 'station')
    search_fields = ('title',)
    list_filter = ('station',)

@admin.register(Episode)
class EpisodeAdmin(admin.ModelAdmin):
    list_display = ('episode_id', 'webtoon', 'episode_num', 'subtitle')
    search_fields = ('subtitle', 'webtoon__title') 
    list_filter = ('webtoon',)

@admin.register(Cut)
class CutAdmin(admin.ModelAdmin):
    list_display = ('cut_id', 'episode', 'cut_order', 'image_preview')
    list_filter = ('episode__webtoon', 'episode')
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        if not obj.image:
            return "No Image"
        
        if hasattr(obj.image, 'url'):
            try:
                return mark_safe(f'<img src="{obj.image.url}" width="100" />')
            except:
                pass
        
        image_path = str(obj.image)
        if image_path.startswith('s3://'):
            path_only = image_path.replace('s3://hisub-s3-bucket/', '')
            image_url = f"https://hisub-s3-bucket.s3.ap-northeast-2.amazonaws.com/{path_only}"
        else:
            image_url = image_path

        return mark_safe(f'<img src="{image_url}" width="100" />')

    image_preview.short_description = "미리보기"

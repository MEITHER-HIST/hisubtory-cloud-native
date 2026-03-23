from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Webtoon, Episode, Cut
from .serializers import get_presigned_url

@admin.register(Webtoon)
class WebtoonAdmin(admin.ModelAdmin):
    list_display = ('webtoon_id', 'title', 'station', 'thumbnail_preview')
    search_fields = ('title',)

    def thumbnail_preview(self, obj):
        if obj.thumbnail:
            url = get_presigned_url(obj.thumbnail)
            return mark_safe(f'<img src="{url}" width="100" />')
        return "-"
    thumbnail_preview.short_description = 'Thumbnail Preview'

@admin.register(Episode)
class EpisodeAdmin(admin.ModelAdmin):
    list_display = ('episode_id', 'webtoon', 'episode_num', 'subtitle', 'source_preview')
    list_filter = ('webtoon',)
    search_fields = ('subtitle',)

    def source_preview(self, obj):
        if obj.source_url:
            url = get_presigned_url(obj.source_url)
            return mark_safe(f'<img src="{url}" width="100" />')
        return "-"
    source_preview.short_description = 'Source Preview'

@admin.register(Cut)
class CutAdmin(admin.ModelAdmin):
    list_display = ('cut_id', 'episode', 'cut_order', 'image_preview')
    list_filter = ('episode',)
    
    def image_preview(self, obj):
        if obj.image:
            url = get_presigned_url(obj.image)
            return mark_safe(f'<img src="{url}" width="100" />')
        return "-"
    image_preview.short_description = 'Image Preview'

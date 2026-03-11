from django.contrib import admin
from .models import Webtoon, Episode, Cut

@admin.register(Webtoon)
class WebtoonAdmin(admin.ModelAdmin):
    list_display = ('webtoon_id', 'title', 'station')
    search_fields = ('title',)

@admin.register(Episode)
class EpisodeAdmin(admin.ModelAdmin):
    list_display = ('episode_id', 'webtoon', 'episode_num', 'subtitle')
    list_filter = ('webtoon',)
    search_fields = ('subtitle',)

@admin.register(Cut)
class CutAdmin(admin.ModelAdmin):
    list_display = ('cut_id', 'episode', 'cut_order')
    list_filter = ('episode',)

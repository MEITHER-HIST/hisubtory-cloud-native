from django.contrib import admin
from .models import Bookmark, UserViewedEpisode

@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'episode_id', 'created_at')
    search_fields = ('user__username', 'episode_id')
    list_filter = ('created_at',)

@admin.register(UserViewedEpisode)
class UserViewedEpisodeAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'episode_id', 'viewed_at')
    search_fields = ('user__username', 'episode_id')
    list_filter = ('viewed_at',)

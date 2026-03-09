from django.db import models
from django.conf import settings
from stories.models import Episode

User = settings.AUTH_USER_MODEL

# --- 사용자가 본 에피소드 기록 (Supabase.png의 파란 박스 관계 설계) ---
class UserViewedEpisode(models.Model):
    # user_id 필드가 데이터베이스의 accounts_user(id)를 명확하게 참조하도록 설정
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='viewed_episodes', 
        db_column='user_id' # DB의 컬럼명과 일치
    )
    episode_id = models.BigIntegerField() # MySQL의 episode_id 참조 (물리적 제약 없이 로직으로 관리)
    viewed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "library_userviewedepisode"
        unique_together = ('user', 'episode_id')
        managed = True
        app_label = 'library'

    def __str__(self):
        return f"{self.user.username} - 시청 기록 (ID: {self.episode_id})"


# --- 북마크 모델 (Supabase.png의 파란 박스 관계 설계) ---
class Bookmark(models.Model):
    # user_id 필드가 데이터베이스의 accounts_user(id)를 명확하게 참조하도록 설정
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='bookmarks', 
        db_column='user_id' # DB의 컬럼명과 일치
    )
    episode_id = models.BigIntegerField() # MySQL의 episode_id 참조 (물리적 제약 없이 로직으로 관리)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "library_bookmark"
        unique_together = ('user', 'episode_id')
        managed = True
        app_label = 'library'

    def __str__(self):
        return f"{self.user.username} - 북마크 (ID: {self.episode_id})"

from django.db import models
from django.contrib.auth.models import AbstractBaseUser

class User(AbstractBaseUser):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'

    class Meta:
        db_table = 'accounts_user'
        managed = False

class Line(models.Model):
    id = models.BigAutoField(primary_key=True)
    line_name = models.CharField(max_length=100)

    class Meta:
        db_table = "subway_line"
        managed = False

class Station(models.Model):
    id = models.BigAutoField(primary_key=True)
    station_name = models.CharField(max_length=100)

    class Meta:
        db_table = "subway_station"
        managed = False

class Webtoon(models.Model):
    webtoon_id = models.BigAutoField(primary_key=True)
    station = models.ForeignKey(Station, on_delete=models.DO_NOTHING, db_column='station_id')
    title = models.CharField(max_length=200)
    thumbnail = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        db_table = "webtoons"
        managed = False

class Episode(models.Model):
    episode_id = models.BigAutoField(primary_key=True)
    webtoon = models.ForeignKey(Webtoon, on_delete=models.DO_NOTHING, related_name='episodes', db_column='webtoon_id')
    episode_num = models.IntegerField()
    subtitle = models.CharField(max_length=255)
    source_url = models.URLField(blank=True, null=True)

    class Meta:
        db_table = "episodes"
        managed = False

class Cut(models.Model):
    cut_id = models.BigAutoField(primary_key=True)
    episode = models.ForeignKey(Episode, on_delete=models.DO_NOTHING, related_name="cuts", db_column='episode_id')
    image = models.CharField(max_length=255)
    caption = models.TextField(blank=True, null=True)
    cut_order = models.SmallIntegerField()

    class Meta:
        db_table = "cuts"
        managed = False

class UserViewedEpisode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='viewed_episodes')
    episode = models.ForeignKey(Episode, on_delete=models.CASCADE)
    viewed_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = "library_userviewedepisode"
        unique_together = ('user', 'episode')
        managed = False

class Bookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookmarks')
    episode = models.ForeignKey(Episode, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = "library_bookmark"
        unique_together = ('user', 'episode')
        managed = False

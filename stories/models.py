from django.db import models
from subway.models import Station

def get_cut_image_path(instance, filename):
    return f"webtoons/{instance.episode.webtoon.webtoon_id}/episodes/{instance.episode.episode_id}/cuts/{filename}"

class Webtoon(models.Model):
    webtoon_id = models.BigAutoField(primary_key=True)
    station = models.ForeignKey(Station, on_delete=models.CASCADE, db_column='station_id')
    title = models.CharField(max_length=200)
    thumbnail = models.CharField(max_length=500, blank=True, null=True)

    @property
    def thumbnail_url(self):
        from .serializers import get_presigned_url
        return get_presigned_url(self.thumbnail)

    class Meta:
        db_table = "webtoons"
        managed = True
        app_label = 'stories'

    def __str__(self):
        return self.title

class Episode(models.Model):
    episode_id = models.BigAutoField(primary_key=True)
    webtoon = models.ForeignKey(Webtoon, on_delete=models.CASCADE, related_name='episodes', db_column='webtoon_id')
    episode_num = models.IntegerField()
    subtitle = models.CharField(max_length=255)
    source_url = models.CharField(max_length=500, blank=True, null=True)

    @property
    def source_url_val(self):
        from .serializers import get_presigned_url
        return get_presigned_url(self.source_url)

    class Meta:
        db_table = "episodes"
        managed = True
        app_label = 'stories'

    def __str__(self):
        return f"[{self.webtoon.title}] {self.episode_num}화: {self.subtitle}"

class Cut(models.Model):
    cut_id = models.BigAutoField(primary_key=True)
    episode = models.ForeignKey(Episode, on_delete=models.CASCADE, related_name="cuts", db_column='episode_id')
    image = models.CharField(max_length=500) 
    caption = models.TextField(blank=True, null=True)
    cut_order = models.SmallIntegerField()

    @property
    def image_url(self):
        from .serializers import get_presigned_url
        return get_presigned_url(self.image)

    class Meta:
        db_table = "cuts"
        managed = True
        app_label = 'stories'

    def __str__(self):
        return f"{self.episode.subtitle} - 컷 {self.cut_order}"

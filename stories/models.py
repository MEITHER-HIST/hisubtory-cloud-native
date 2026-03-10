from django.db import models
from subway.models import Station

class Webtoon(models.Model):
    webtoon_id = models.BigAutoField(primary_key=True)
    station = models.ForeignKey(Station, on_delete=models.CASCADE, db_column='station_id')
    title = models.CharField(max_length=200)
    thumbnail = models.ImageField(upload_to="webtoons/thumbnails/", blank=True, null=True)

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
    source_url = models.URLField(blank=True, null=True)

    class Meta:
        db_table = "episodes"
        managed = True
        app_label = 'stories'

    def __str__(self):
        return f"[{self.webtoon.title}] {self.episode_num}화: {self.subtitle}"

class Cut(models.Model):
    cut_id = models.BigAutoField(primary_key=True)
    episode = models.ForeignKey(Episode, on_delete=models.CASCADE, related_name="cuts", db_column='episode_id')
    image = models.CharField(max_length=255) 
    caption = models.TextField(blank=True, null=True)
    cut_order = models.SmallIntegerField()

    class Meta:
        db_table = "cuts"
        managed = True
        app_label = 'stories'

    def __str__(self):
        return f"{self.episode.subtitle} - 컷 {self.cut_order}"

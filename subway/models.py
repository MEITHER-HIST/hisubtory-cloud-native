# subway/models.py
from django.db import models

class Line(models.Model):
    line_name = models.CharField(max_length=50, unique=True)
    line_color = models.CharField(max_length=7, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = 'subway'

    def __str__(self):
        return self.line_name

class Station(models.Model):
    station_code = models.CharField(max_length=50, unique=True, blank=True, null=True)
    station_name = models.CharField(max_length=100)
    is_enabled = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    lines = models.ManyToManyField(Line, related_name='stations', blank=True)

    class Meta:
        app_label = 'subway'

    def __str__(self):
        return self.station_name

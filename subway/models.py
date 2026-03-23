from django.db import models

class Line(models.Model):
    line_name = models.CharField(max_length=50, unique=True)
    line_color = models.CharField(max_length=7, blank=True, null=True)
    stations = models.ManyToManyField('Station', related_name='lines', db_table='subway_station_lines')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'subway_line'

    def __str__(self):
        return self.line_name

class Station(models.Model):
    station_code = models.CharField(max_length=50, unique=True, blank=True, null=True)
    station_name = models.CharField(max_length=100)
    is_enabled = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'subway_station'

    def __str__(self):
        return self.station_name

from django.contrib import admin
from .models import Line, Station

@admin.register(Line)
class LineAdmin(admin.ModelAdmin):
    list_display = ('id', 'line_name', 'line_color')
    search_fields = ('line_name',)

@admin.register(Station)
class StationAdmin(admin.ModelAdmin):
    list_display = ('id', 'station_code', 'station_name', 'is_enabled')
    list_filter = ('lines', 'is_enabled')
    search_fields = ('station_name', 'station_code')

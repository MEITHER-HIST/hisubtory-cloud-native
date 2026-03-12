from django.http import HttpResponse
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse
from django_prometheus import exports

def health(request):
    return HttpResponse("ok", content_type="text/plain")

urlpatterns = [
    path('health/', lambda r: HttpResponse('OK', status=200)),
    path("api/stories/", include("stories.urls")),
    path("api/library/", include("library.urls")),
    path("library/", include("library.urls")),
    path("", include("stories.urls")),

    # 시스템 및 모니터링
    path("metrics", exports.ExportToDjangoView, name="prometheus-metrics"),
    path("metrics/", exports.ExportToDjangoView),
    path("health/", health),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

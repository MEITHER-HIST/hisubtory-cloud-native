from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse
from django_prometheus import exports

def health(request):
    return HttpResponse("ok", content_type="text/plain")

urlpatterns = [
    # 1. API 전용 경로
    path("api/pages/", include("pages.urls_api")),
    path("api/library/", include("library.urls")),
    path("library/", include("library.urls")),
    
    # 2. 시스템 및 모니터링
    path("metrics", exports.ExportToDjangoView, name="prometheus-metrics"),
    path("metrics/", exports.ExportToDjangoView),
    path("health/", health),
    path("", health),
    path("admin/", admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

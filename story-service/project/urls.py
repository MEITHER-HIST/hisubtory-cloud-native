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
    # Nginx가 /api/stories/ 를 떼지 않고 그대로 전달하므로, 
    # 여기서도 /api/stories/ 로 시작하는 경로를 받아야 합니다.
    path("api/stories/", include("stories.urls")),
    
    # 만약 Nginx 설정에 따라 /api/stories/가 이미 제거된 상태라면 아래 경로가 작동합니다.
    path("", include("stories.urls")),

    # 시스템 및 모니터링
    path("metrics", exports.ExportToDjangoView, name="prometheus-metrics"),
    path("metrics/", exports.ExportToDjangoView),
    path("health/", health),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

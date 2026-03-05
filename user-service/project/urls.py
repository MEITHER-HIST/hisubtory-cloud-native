from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse
from django.shortcuts import render

def health(request):
    return HttpResponse("ok", content_type="text/plain")

def index(request):
    return render(request, "main.html")

urlpatterns = [
    # 1. 시스템 및 어드민
    path("", index, name="index"),
    path("health/", health),
    path("admin/", admin.site.urls),
    path("favicon.ico", lambda r: HttpResponse(status=204)),

    # 2. API 전용 경로
    path("api/accounts/", include("accounts.urls_api")),
    path("api/stories/", include("stories.urls_api")),
    path("api/library/", include("library.urls")),
    # pages는 activity-service에서 담당하므로 Nginx가 라우팅하지만, 
    # 로컬 개발 편의를 위해 포함 (activity-service가 PYTHONPATH에 있어야 함)
    path("api/pages/", include("pages.urls_api")),

    # 3. HTML/Legacy 경로
    path("accounts/", include("accounts.urls")),
    path("stories/", include("stories.urls")),
    path("library/", include("library.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

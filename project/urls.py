from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse
from django.shortcuts import render

# Final deployment trigger with updated AWS keys
def health(request):
    return HttpResponse("ok", content_type="text/plain")

def index(request):
    return render(request, "main.html")

urlpatterns = [
    path("", index, name="index"),
    path("health/", health),
    path("health", health),
    path("admin/", admin.site.urls),
    path("favicon.ico", lambda r: HttpResponse(status=204)),

    # 2. API 전용 경로
    path("api/pages/", include("pages.urls")),
    path("api/stories/", include("stories.urls")),
    path("api/library/", include("library.urls")),

    # 3. HTML/Legacy 경로 (기존 템플릿 페이지)
    path("accounts/", include("accounts.urls")),
    path("stories/", include("stories.urls")),
    path("library/", include("library.urls")),
    path("", include("pages.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

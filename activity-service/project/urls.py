from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse
from django_prometheus import exports

def health(request):
    return HttpResponse("ok", content_type="text/plain")

urlpatterns = [
    path('health/', health),
    path("api/pages/", include("pages.urls_api")),
    path("api/bookmarks/", include("library.urls")),
    path("api/library/", include("library.urls")),
    path("metrics", exports.ExportToDjangoView, name="prometheus-metrics"),
    path("metrics/", exports.ExportToDjangoView),
    path("stories/", include("stories.urls")),
    path("library/", include("library.urls")),
    path("", include("pages.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

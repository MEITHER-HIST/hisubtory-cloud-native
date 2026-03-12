from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse

def health(request):
    return HttpResponse("ok")

urlpatterns = [
    path('health/', health),
    path('admin/', admin.site.urls),
    # 💡 어떤 경로로 들어오든(api/pages/ 포함 여부와 상관없이) pages.urls_api에서 처리하도록 합니다.
    path("", include("pages.urls_api")),
]

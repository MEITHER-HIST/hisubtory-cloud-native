from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse

def health(request):
    return HttpResponse("ok")

urlpatterns = [
    path('health/', health),
    path('admin/', admin.site.urls),
    # 💡 이미 Nginx에서 /api/pages/ 를 붙여서 보내므로, include 시 prefix를 비웁니다.
    path("", include("pages.urls_api")),
]

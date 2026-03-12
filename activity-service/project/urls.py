from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse

def health(request):
    return HttpResponse("ok")

urlpatterns = [
    path('health/', health),
    path('admin/', admin.site.urls),
    # 💡 이미 Nginx에서 /api/pages/ 를 붙여서 보내거나 떼서 보낼 수 있으므로 둘 다 처리
    path("api/pages/", include("pages.urls_api")),
    path("", include("pages.urls_api")),
]

from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse

urlpatterns = [
    path('health/', lambda r: HttpResponse('ok')),
    path('admin/', admin.site.urls),
    # 💡 루트에서 바로 pages.urls_api를 매핑하여 Nginx prefixes와 상관없이 동작하게 함
    path("", include("pages.urls_api")),
]

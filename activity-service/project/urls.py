from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse

urlpatterns = [
    path('health/', lambda r: HttpResponse('ok')),
    path('admin/', admin.site.urls),
    # 💡 루트와 api/pages/ 둘 다 매핑하여 유연하게 대응
    path("", include("pages.urls_api")),
    path("api/pages/", include("pages.urls_api")),
]

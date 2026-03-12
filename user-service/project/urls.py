from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse

urlpatterns = [
    path('health/', lambda r: HttpResponse('ok')),
    path('admin/', admin.site.urls),
    # 💡 이미 Nginx에서 /api/accounts/ 를 붙여서 보내거나 떼서 보낼 수 있으므로 둘 다 처리
    path("api/accounts/", include("accounts.urls_api")),
    path("api/library/", include("library.urls")),
    path("library/", include("library.urls")),
    path("", include("accounts.urls_api")),
]

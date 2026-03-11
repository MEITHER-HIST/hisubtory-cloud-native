from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse

def health(request):
    return HttpResponse("ok")

urlpatterns = [
    path('health/', health),
    path("api/pages/", include("pages.urls_api")),
    path("api/accounts/", include("accounts.urls_api")),
    path("api/stories/", include("pages.urls_api")), # 임시: 에러 방지를 위해 pages쪽 참조
]

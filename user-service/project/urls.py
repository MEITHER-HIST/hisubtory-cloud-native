from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse

def health(request):
    return HttpResponse("ok")

urlpatterns = [
    path('health/', health),
    path("api/accounts/", include("accounts.urls_api")),
    path("admin/", admin.site.urls),
]

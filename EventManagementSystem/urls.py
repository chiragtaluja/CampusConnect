from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static 

urlpatterns = [
    path("admin/", admin.site.urls), 
    path("", include("base.urls")),
    path("__reload__/", include("django_browser_reload.urls")),
    
    ]

if settings.DEBUG:
    # Include django_browser_reload URLs only in DEBUG mode
    urlpatterns += [
        path("__reload__/", include("django_browser_reload.urls")),
    ]
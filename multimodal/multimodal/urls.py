from django.contrib import admin
from django.conf.urls import include
from django.views.static import serve
from django.urls import path, re_path

from . import settings
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('whisper.urls')),
    path('', include('filemanager.urls')),
    path(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),
    path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
]+static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

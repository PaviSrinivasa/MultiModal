from django.urls import re_path as url
from django.urls import path, re_path, include

from .views import file_maniputer

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('whisper/', views.whisper, name='whisper'),
    url(r'^file_maniputer_api$', file_maniputer),
    path('filebrowser/', views.file_browser, name='file_browser'),
]

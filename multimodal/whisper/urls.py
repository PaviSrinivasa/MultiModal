from django.conf.urls import url
from django.urls import path, re_path, include

from .views import file_maniputer

from . import views

urlpatterns = [
    path('multimodal/', views.home, name='home'),
    path('multimodal/multimodalaccounts/', include('django.contrib.auth.urls')),
    url(r'multimodal/^file_maniputer_api$', file_maniputer),
]

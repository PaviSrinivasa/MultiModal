from django.conf.urls import include
from django.urls import path, re_path

from .views import file_maniputer,file_browserJSON
from filemanager import FileManager, path_end

from . import views

#pathFolder='/mnt/c/Users/pavsri/Documents/GitHub/MultiModalProject'

urlpatterns = [
    path('', views.home, name='home'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('whisper/', views.whisper, name='whisper'),
    re_path(r'^file_maniputer_api$', file_maniputer),
    path('filebrowser', views.file_browser, name='file_browser'),
    path('filepicker', views.filepicker, name='filepicker'),
    path('beverage', views.beverage, name='beverage'),
    path('filebrowserJSON', views.file_browserJSON, name='file_browserJSON'),
    path(r'^popup/$', views.file_browserJSON, name='popup'),
    #path(r'^fb/'+path_end, views.view, name='view'),
    #path(r'^pop/$'+ path_end, views.view, name='view'),
    path('', include('filemanager.urls')),

]

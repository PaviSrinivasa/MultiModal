from django.urls import include, re_path
from django.conf import settings
from django.conf.urls.static import static
from filemanager import path_end

from .views import view

urlpatterns = [
   re_path(r'^fb/' + path_end, view, name='view'),
 ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

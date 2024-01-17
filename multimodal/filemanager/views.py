from filemanager import FileManager
from django.conf import settings

#path = '/mnt/d/Docs'

def view(request, path):
    extensions = ['html', 'htm', 'zip', 'py', 'css', 'js', 'jpeg', 'jpg', 'png', 'pdf']
    fm = FileManager( settings.MEDIA_ROOT, extensions=extensions)
    return fm.render(request, path)

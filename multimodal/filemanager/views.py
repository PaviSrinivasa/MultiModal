from filemanager import FileManager
from django.conf import settings

#path = '/mnt/d/Docs'

def view(request, path):
    extensions = ['html', 'htm', 'zip', 'py', 'css', 'js', 'jpeg', 'jpg', 'png', 'pdf']
    print('View')
    folder_path = request.GET.get('folder')
    print('folder_path',folder_path)
    print('View-Path',path)
    fm = FileManager(settings.MEDIA_ROOT, extensions=extensions)
    return fm.render(request, path)

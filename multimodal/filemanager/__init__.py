import pathlib

from django.shortcuts import render
from django.http import HttpResponse
from django import forms
from PIL import Image
from . import settings
import mimetypes
import os
import shutil
import re
import tarfile
import zipfile
import magic
import posixpath

path_end = r'(?P<path>[\w\d_ -/.]*)$'

ActionChoices = (
    ('upload', 'upload'),
    ('rename', 'rename'),
    ('delete', 'delete'),
    ('add', 'add'),
    ('move', 'move'),
    ('copy', 'copy'),
    ('unzip', 'unzip'),
)


class FileManagerForm(forms.Form):
    ufile = forms.FileField(required=False)
    action = forms.ChoiceField(choices=ActionChoices)
    path = forms.CharField(max_length=200, required=False)
    name = forms.CharField(max_length=32, required=False)
    current_path = forms.CharField(max_length=200, required=False)
    file_or_dir = forms.CharField(max_length=4)


class FileManager(object):
    """
    maxspace,maxfilesize in KB
    """

    def __init__(
            self,
            basepath,
            extensions=None,
    ):
        print('basepath: ',basepath)
        self.basepath = basepath
        self.folder = basepath
        self.extensions = extensions


    def rename_if_exists(self, folder, file):
        if folder[-1] != os.sep:
            folder = folder + os.sep
        if os.path.exists(folder + file):
            if file.find('.') == -1:
                # no extension
                for i in range(1000):
                    if not os.path.exists(folder + file + '.' + str(i)):
                        break
                return file + '.' + str(i)
            else:
                extension = file[file.rfind('.'):]
                name = file[:file.rfind('.')]
                for i in range(1000):
                    full_path = folder + name + '.' + str(i) + extension
                    if not os.path.exists(full_path):
                        break
                return name + '.' + str(i) + extension
        else:
            return file

    def get_size(self, start_path):
        total_size = 0
        for dirpath, dirnames, filenames in os.walk(start_path):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                total_size += os.path.getsize(fp)
        return total_size

    def handle_form(self, form, files):
        action = form.cleaned_data['action']
        path = form.cleaned_data['path']
        name = form.cleaned_data['name']
        file_or_dir = form.cleaned_data['file_or_dir']
        self.current_path = form.cleaned_data['current_path']
        messages = []
        invalid_path = not re.match(r'[\w\d_ -/]+', path).group(0) == path
        if invalid_path:
            messages.append("Invalid path : " + path)
            return messages

        return messages

    def directory_structure(self, start_point):
        if not start_point:
            start_point = self.basepath
        else:
            start_point = self.folder
        print('start point', start_point)
        os.chdir(start_point)
        dir_listing = []
        file_listing = []
        name_folders = []

        iterDir = 0
        iterFile = 0

        for list_of_contents in os.scandir(start_point):
            if list_of_contents.is_dir():
                if not dir_listing:
                    dir_listing = [list_of_contents.path]
                    name_folders = [list_of_contents.name]
                else:
                    iter+=1
                    dir_listing.append(list_of_contents.path)
                    name_folders.append(list_of_contents.name)
            else:
                if not file_listing:
                    file_listing = [list_of_contents.path]
                else:
                    file_listing.append(list_of_contents.path)

        print('dir_listing: ', dir_listing)
        print('file_listing: ', file_listing)
        print('name_folders: ', name_folders)

        dir_contents = posixpath.normpath(start_point)

        dir_structure = {
            dir_contents : {
                'open': 'yes',
                'dirs': dir_listing,
                'files': file_listing,
                'name': name_folders
            }
        }

        print('dir_structure: ', dir_structure)

        return dir_structure



        # for directory, directories, files in os.walk('.'):
        #       directory_list = directory[1:].split('/')
        #       current_dir = None
        #       nextdirs = dir_structure
        #       for d in directory_list:
        #           current_dir = nextdirs[d]
        #           nextdirs = current_dir['dirs']
        #       if directory[1:] + '/' == self.current_path:
        #           self.current_id = current_dir['id']
        #       current_dir['dirs'].update(
        #          dict(
        #              map(
        #                  lambda d: (
        #                      d,
        #                      {
        #                         'id': self.next_id(),
        #                          'open': 'no',
        #                          'dirs': {},
        #                          'files': [],
        #                     }
        #                  ),
        #                  directories,
        #              )
        #          )
        #       )
        #       current_dir['files'] = files
        # return dir_structure

# print(os.listdir('.'))
        # for content_list in os.listdir('.'):
        #     nextdirs = dir_structure
        # dict_list = []
        # current_dir = dir_structure
        # for d in os.scandir(self.basepath):
        #     print('Scan: ', d)
        #     if len(dict_list) == 0:
        #         dict_list = d.path
        #     else:
        #         dict_list = dict_list.update(d.path)
        #     print('dict_list: ', dict_list)
        #     if d.is_dir():
        #         current_dir['open'] = 'no'
        #         current_dir['dirs']= d.path
        #     if d.is_file():
        #         current_dir['files']= d.path
        # return dir_structure

    def media(self, path):
        ext = path.split('.')[-1]
        try:
            mimetypes.init()
            mimetype = mimetypes.guess_type(path)[0]
            img = Image.open(self.basepath + '/' + path)
            width, height = img.size
            mx = max([width, height])
            w, h = width, height
            if mx > 60:
                w = width * 60 / mx
                h = height * 60 / mx
            img = img.resize((w, h), Image.Resampling.LANCZOS)
            response = HttpResponse(content_type=mimetype or "image/" + ext)
            response['Cache-Control'] = 'max-age=3600'
            img.save(
                response,
                mimetype.split('/')[1] if mimetype else ext.upper()
            )
            return response
        except Exception:
            imagepath = (
                    settings.FILEMANAGER_STATIC_ROOT
                    + 'images/icons/'
                    + ext
                    + '.png'
            )
            if not os.path.exists(imagepath):
                imagepath = (
                        settings.FILEMANAGER_STATIC_ROOT
                        + 'images/icons/default.png'
                )
            img = Image.open(imagepath)
            width, height = img.size
            mx = max([width, height])
            w, h = width, height
            if mx > 60:
                w = int(width * 60 / mx)
                h = int(height * 60 / mx)
            img = img.resize((w, h), Image.Resampling.LANCZOS)
            response = HttpResponse(content_type="image/png")
            response['Cache-Control'] = 'max-age:3600'
            img.save(response, 'png')
            return response

    def render(self, request, path):
        messages = []
        if path:
            return self.media(path)
        self.current_path = '/'
        self.current_id = 1
        print('self.folder: ', self.folder)
        print('path', path)
        if request.method == 'POST':
            form = FileManagerForm(request.POST, request.FILES)
            if form.is_valid():
                messages = self.handle_form(form, request.FILES)
        print('before render')
        return render(
            request,
            'filemanager/index.html',
            {
                'dir_structure': self.directory_structure(path),
                'messages': list(map(str, messages)),
                'current_id': self.current_id,
                'folder': self.folder,
            }
        )

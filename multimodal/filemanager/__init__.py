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
    idee = 0

    def __init__(
            self,
            basepath,
            ckeditor_baseurl='',
            maxfolders=500,
            maxspace=500 * 1024,
            maxfilesize=500 * 1024,
            public_url_base=None,
            extensions=None,
    ):
        # if basepath[-1] == '/':
      #      basepath = basepath[:-1]
        if ckeditor_baseurl and ckeditor_baseurl[-1] == '/':
            ckeditor_baseurl = ckeditor_baseurl[:-1]
        self.basepath = basepath
        self.ckeditor_baseurl = ckeditor_baseurl
        self.maxfolders = maxfolders
        self.maxspace = maxspace
        self.maxfilesize = maxfilesize
        self.extensions = extensions
        self.public_url_base = public_url_base

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

    def next_id(self):
        self.idee = self.idee + 1
        return self.idee

    def handle_form(self, form, files):
        action = form.cleaned_data['action']
        path = form.cleaned_data['path']
        name = form.cleaned_data['name']
        file_or_dir = form.cleaned_data['file_or_dir']
        self.current_path = form.cleaned_data['current_path']
        messages = []

        invalid_folder_name = (
                name
                and file_or_dir == 'dir'
                and not re.match(r'[\w\d_ -]+', name).group(0) == name
        )
        if invalid_folder_name:
            messages.append("Invalid folder name : " + name)
            return messages

        invalid_file_name = (
                name
                and file_or_dir == 'file'
                and (
                        re.search(r'\.\.', name)
                        or not re.match(r'[\w\d_ -.]+', name).group(0) == name
                )
        )
        if invalid_file_name:
            messages.append("Invalid file name : " + name)
            return messages

        invalid_path = not re.match(r'[\w\d_ -/]+', path).group(0) == path
        if invalid_path:
            messages.append("Invalid path : " + path)
            return messages
        if action == 'upload':
            for f in files.getlist('ufile'):
                file_name_invalid = (
                        re.search(r'\.\.', f.name)
                        or not re.match(r'[\w\d_ -/.]+', f.name).group(0) == f.name
                )
                if file_name_invalid:
                    messages.append("File name is not valid : " + f.name)
                elif f.size > self.maxfilesize * 1024:
                    messages.append(
                        "File size exceeded "
                        + str(self.maxfilesize)
                        + " KB : "
                        + f.name
                    )
                elif (
                        settings.FILEMANAGER_CHECK_SPACE and
                        (
                                (self.get_size(self.basepath) + f.size)
                                > self.maxspace * 1024
                        )
                ):
                    messages.append(
                        "Total Space size exceeded "
                        + str(self.maxspace)
                        + " KB : "
                        + f.name
                    )
                elif (
                        self.extensions
                        and len(f.name.split('.')) > 1
                        and f.name.split('.')[-1] not in self.extensions
                ):
                    messages.append(
                        "File extension not allowed (."
                        + f.name.split('.')[-1]
                        + ") : "
                        + f.name
                    )
                elif (
                        self.extensions
                        and len(f.name.split('.')) == 1
                        and f.name.split('.')[-1]
                        not in self.extensions
                ):
                    messages.append(
                        "No file extension in uploaded file : "
                        + f.name
                    )
                else:
                    filename = f.name.replace(' ', '_')  # replace spaces to prevent fs error
                    filepath = os.path.join(
                            self.basepath,
                            path,
                            self.rename_if_exists(os.path.join(self.basepath, path, filename))
                    )
                    with open(filepath, 'wb') as dest:
                        for chunk in f.chunks():
                            dest.write(chunk)
                    f.close()
                    mimetype = magic.from_file(filepath, mime=True)
                    guessed_exts = mimetypes.guess_all_extensions(mimetype)
                    guessed_exts = [ext[1:] for ext in guessed_exts]
                    common = [ext for ext in guessed_exts if ext in self.extensions]
                    if not common:
                        os.remove(filepath)
                        messages.append(
                            "File type not allowed : "
                            + f.name
                        )
            if len(messages) == 0:
                messages.append('All files uploaded successfully')
        elif action == 'add':
            os.chdir(self.basepath)
            no_of_folders = len(list(os.walk('.')))
            if (no_of_folders + 1) <= self.maxfolders:
                try:
                    os.chdir(self.basepath + path)
                    os.mkdir(name)
                    messages.append('Folder created successfully : ' + name)
                except OSError:
                    messages.append('Folder couldn\'t be created : ' + name)
                except Exception as e:
                    messages.append('Unexpected error : ' + e)
            else:
                messages.append(
                    'Folder couldn\' be created because maximum number of '
                    + 'folders exceeded : '
                    + str(self.maxfolders)
                )
        elif action == 'rename' and file_or_dir == 'dir':
            oldname = path.split('/')[-2]
            path = '/'.join(path.split('/')[:-2])
            try:
                os.chdir(self.basepath + path)
                os.rename(oldname, name)
                messages.append(
                    'Folder renamed successfully from '
                    + oldname
                    + ' to '
                    + name
                )
            except OSError:
                messages.append('Folder couldn\'t renamed to ' + name)
            except Exception as e:
                messages.append('Unexpected error : ' + e)
        elif action == 'delete' and file_or_dir == 'dir':
            if path == '/':
                messages.append('root folder can\'t be deleted')
            else:
                name = path.split('/')[-2]
                path = '/'.join(path.split('/')[:-2])
                try:
                    os.chdir(self.basepath + path)
                    shutil.rmtree(name)
                    messages.append('Folder deleted successfully : ' + name)
                except OSError:
                    messages.append('Folder couldn\'t deleted : ' + name)
                except Exception as e:
                    messages.append('Unexpected error : ' + e)
        elif action == 'rename' and file_or_dir == 'file':
            oldname = path.split('/')[-1]
            old_ext = (
                oldname.split('.')[1]
                if len(oldname.split('.')) > 1
                else None
            )
            new_ext = name.split('.')[1] if len(name.split('.')) > 1 else None
            if old_ext == new_ext:
                path = '/'.join(path.split('/')[:-1])
                try:
                    os.chdir(self.basepath + path)
                    os.rename(oldname, name)
                    messages.append(
                        'File renamed successfully from '
                        + oldname
                        + ' to '
                        + name
                    )
                except OSError:
                    messages.append('File couldn\'t be renamed to ' + name)
                except Exception as e:
                    messages.append('Unexpected error : ' + e)
            else:
                if old_ext:
                    messages.append(
                        'File extension should be same : .'
                        + old_ext
                    )
                else:
                    messages.append(
                        'New file extension didn\'t match with old file'
                        + ' extension'
                    )
        elif action == 'delete' and file_or_dir == 'file':
            if path == '/':
                messages.append('root folder can\'t be deleted')
            else:
                name = path.split('/')[-1]
                path = '/'.join(path.split('/')[:-1])
                try:
                    os.chdir(self.basepath + path)
                    os.remove(name)
                    messages.append('File deleted successfully : ' + name)
                except OSError:
                    messages.append('File couldn\'t deleted : ' + name)
                except Exception as e:
                    messages.append('Unexpected error : ' + e)
        elif action == 'move' or action == 'copy':
            # from path to current_path
            if self.current_path.find(path) == 0:
                messages.append('Cannot move/copy to a child folder')
            else:
                path = os.path.normpath(path)  # strip trailing slash if any
                filename = (
                        self.basepath
                        + self.current_path
                        + os.path.basename(path)
                )
                if os.path.exists(filename):
                    messages.append(
                        'ERROR: A file/folder with this name already exists in'
                        + ' the destination folder.'
                    )
                else:
                    if action == 'move':
                        method = shutil.move
                    else:
                        if file_or_dir == 'dir':
                            method = shutil.copytree
                        else:
                            method = shutil.copy
                    try:
                        method(self.basepath + path, filename)
                    except OSError:
                        messages.append(
                            'File/folder couldn\'t be moved/copied.'
                        )
                    except Exception as e:
                        messages.append('Unexpected error : ' + e)
        elif action == 'unzip':
            if file_or_dir == 'dir':
                messages.append('Cannot unzip a directory')
            else:
                try:
                    path = os.path.normpath(path)  # strip trailing slash if any
                    filename = (
                            self.basepath
                            + self.current_path
                            + os.path.basename(path)
                    )
                    zip_ref = zipfile.ZipFile(filename, 'r')
                    # zip_ref.extractall(self.basepath + self.current_path)
                    directory = self.basepath + self.current_path
                    for file in zip_ref.namelist():
                        if file.endswith(tuple(self.extensions)):
                            zip_ref.extract(file, directory)
                            mimetype = magic.from_file(directory + file, mime=True)
                            print(directory + file)
                            guessed_exts = mimetypes.guess_all_extensions(mimetype)
                            guessed_exts = [ext[1:] for ext in guessed_exts]
                            common = [ext for ext in guessed_exts if ext in self.extensions]
                            if not common:
                                os.remove(directory + file)
                                messages.append(
                                    "File in the zip is not allowed : "
                                    + file
                                )
                    zip_ref.close()
                except Exception as e:
                    print(e)
                    messages.append('ERROR : Could not unzip the file.')
                if len(messages) == 0:
                    messages.append('Extraction completed successfully.')

        return messages

    def directory_structure(self):
        self.idee = 0
        dir_structure = {
            '': {
                'id': self.next_id(),
                'open': 'yes',
                'dirs': {},
                'files': [],
            },
        }
        os.chdir(self.basepath)
        for directory, directories, files in os.walk('.'):
            directory_list = directory[1:].split('/')
            current_dir = None
            nextdirs = dir_structure
            for d in directory_list:
                current_dir = nextdirs[d]
                nextdirs = current_dir['dirs']
            if directory[1:] + '/' == self.current_path:
                self.current_id = current_dir['id']
            current_dir['dirs'].update(
                dict(
                    map(
                        lambda d: (
                            d,
                            {
                                'id': self.next_id(),
                                'open': 'no',
                                'dirs': {},
                                'files': [],
                            }
                        ),
                        directories,
                    )
                )
            )
            current_dir['files'] = files
        return dir_structure

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

    def download(self, path, file_or_dir):
        if not re.match(r'[\w\d_ -/]*', path).group(0) == path:
            return HttpResponse('Invalid path')
        if file_or_dir == 'file':
            filepath = self.basepath + '/' + path
            with open(filepath, 'rb') as f:
                response = HttpResponse(
                    f.read(),
                    content_type=mimetypes.guess_type(filepath)[0],
                )
            response['Content-Length'] = os.path.getsize(filepath)
            response['Content-Disposition'] = (
                    'attachment; filename=' + path.split('/')[-1]
            )
            return response
        elif file_or_dir == 'dir':
            dirpath = self.basepath + '/' + path
            dirname = dirpath.split('/')[-2]
            response = HttpResponse(content_type='application/x-gzip')
            response['Content-Disposition'] = (
                    'attachment; filename=%s.tar.gz'
                    % dirname
            )
            tarred = tarfile.open(fileobj=response, mode='w:gz')
            tarred.add(dirpath, arcname=dirname)
            tarred.close()
            return response

    def render(self, request, path):
        if 'download' in request.GET:
            return self.download(path, request.GET['download'])
        if path:
            return self.media(path)
        CKEditorFuncNum = request.GET.get('CKEditorFuncNum', '')
        messages = []
        self.current_path = '/'
        self.current_id = 1
        if request.method == 'POST':
            form = FileManagerForm(request.POST, request.FILES)
            if form.is_valid():
                messages = self.handle_form(form, request.FILES)
        if settings.FILEMANAGER_CHECK_SPACE:
            space_consumed = self.get_size(self.basepath)
        else:
            space_consumed = 0
        return render(
            request,
            'filemanager/index.html',
            {
                'dir_structure': self.directory_structure(),
                'messages': list(map(str, messages)),
                'current_id': self.current_id,
                'CKEditorFuncNum': CKEditorFuncNum,
                'ckeditor_baseurl': self.ckeditor_baseurl,
                'public_url_base': self.public_url_base,
                'space_consumed': space_consumed,
                'max_space': self.maxspace,
                'show_space': settings.FILEMANAGER_SHOW_SPACE,
            }
        )

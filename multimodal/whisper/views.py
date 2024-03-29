import ast
import json
import os
import re
from subprocess import Popen, PIPE, STDOUT

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from filemanager import FileManager
from filemanager import settings as filesettings

from .forms import WhisperForm
from .models import Whisper


@login_required(login_url='login')
def home(request):
    whiperInfo = Whisper.objects.all().order_by('-id')
    if request.method == 'GET':
     #   myFilter = ExpFilter(request.GET, queryset=expInfo)
      #  expInfo = myFilter.qs
       # return render(request, 'home.html', {'expInfo': expInfo, 'myFilter': myFilter, })
        return render(request, 'home.html', {'whisperInfo':whiperInfo,})
    else:
        return render(request, 'home.html', {})
        #return render(request, 'home.html', {'expInfo': expInfo, })


def whisper(request):
        command = ['qsub test.sge']
        root_directory = os.path.join('/mnt/d/work')
        files = []
        folders = []
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            print(root_directory)
            if os.path.exists(root_directory):
                if( root_directory[ len(root_directory) - 1 ] ==  '/' ):
                    folders = root_directory
                else:
                    folders = root_directory+'/'
                dir1 = dir(root_directory)
                for f in os.walk(root_directory):
                    files.append(f)
            if( len(files) > 2):  #First 2 entries are . and ..  -skip them
                print(files)
                files.sort()
                print(files)
                context = '<ul class="filetree" style="display: none;">'

                for dirpath, dirs, f in os.walk(root_directory):
                    print(dirpath)
                    print (dirs)
                    print(f)
                    context += '<li class="folder collapsed"><a href="#" rel="'+ str(dirpath)+'/">' + str(dirs) + '</a></li>'
                    for file in f:
                        ext = re.sub('/^.*\./', '', file)
                        context += '<li class="file ext_'+ext+'"><a href="#" rel="' +dirpath+'">'+file+'</a></li>'
                context += '</ul>'
            return JsonResponse({'context':context})

        if request.method == 'POST':
                filled_form = WhisperForm(request.POST)
                if filled_form.is_valid():
                        obj = filled_form.save(commit=False)
                        obj.submitter = request.user
                        created_whisper = filled_form.save()
                        messages.success(request, 'Success!')
                else:
                        messages.error(request, 'Failed!')
                new_form = WhisperForm()
                info = Whisper.objects.all()
                return render(request, 'home.html', {})
        else:
                form = WhisperForm()
                return render(request, 'whisper.html', {'addform':form, })


def whisperBrowse(request):
        command = ['qsub test.sge']
        if request.method == 'POST':
                filled_form = WhisperForm(request.POST, request.FILES)
                if filled_form.is_valid():
                        obj = filled_form.save(commit=False)
                        obj.submitter = request.user
                        up_file = request.FILES['upload_file']
                        created_whisper = filled_form.save()
                        messages.success(request, 'Success!')
                else:
                        messages.error(request, 'Failed!')
                new_form = WhisperForm()
                info = Whisper.objects.all()
                return render(request, 'home.html', {})
        else:
                form = WhisperForm()
                return render(request, 'whisper.html', {'addform':form, })

def file_browser1(request):
    root_directory = os.path.join('/mnt/d/work')  # Set the root directory you want to browse
    filepath = []
    directorypath = []

    if os.path.exists(root_directory):
        for dirpath, dirs, files in os.walk(root_directory):
            path = dirpath.split('/')
            directorypath.append('|'+ (len(path))*'---'+ '['+os.path.basename(dirpath)+']')
            for f in files:
                filepath.append('|'+ len(path)*'---'+ f)

    context = {
        'files': filepath,
        'directories': directorypath,
    }
    return render(request, 'browser.html', context)

def file_browser(request):
    root_directory = os.path.join('/mnt/d/work')
    files = []
    folders = []

    if os.path.exists(root_directory):
        if( root_directory[ len(root_directory) - 1 ] ==  '/' ):
            folders = root_directory
        else:
            folders = root_directory+'/'
        dir1 = dir(root_directory)
        for f in os.walk(root_directory):
            files.append(f)

    if( len(files) > 2):  #First 2 entries are . and ..  -skip them
        print(files)
        files.sort()
        print(files)
        context = '<ul class="filetree" style="display: none;">'

        for dirpath, dirs, f in os.walk(root_directory):
            print(dirpath)
            print (dirs)
            print(f)
            context += '<li class="folder collapsed"><a href="#" rel="'+ str(dirpath)+'/">' + str(dirs) + '</a></li>'
            for file in f:
                ext = re.sub('/^.*\./', '', file)
                context += '<li class="file ext_'+ext+'"><a href="#" rel="' +dirpath+'">'+file+'</a></li>'
        context += '</ul>'
    return render(request, 'browser.html', {'context':context})


def file_browserJSON(request):
    context = ''
    root_directory = os.path.join('/mnt/d/work')
    files = []
    folders = []

    if os.path.exists(root_directory):
        if( root_directory[ len(root_directory) - 1 ] ==  '/' ):
            folders = root_directory
        else:
            folders = root_directory+'/'
        dir1 = dir(root_directory)
        for f in os.walk(root_directory):
            files.append(f)

    if( len(files) > 2):  #First 2 entries are . and ..  -skip them
        files.sort()
        print(files)
        context = '<ul class="filetree" style="display: none;">'

        for dirpath, dirs, f in os.walk(root_directory):
            print(dirpath)
            print (dirs)
            print(f)
            context += '<li class="folder collapsed"><a href="#" rel="'+ str(dirpath)+'/">' + str(dirs) + '</a></li>'
            for file in f:
                ext = re.sub('/^.*\./', '', file)
                context += '<li class="file ext_'+ext+'"><a href="#" rel="' +dirpath+'">'+file+'</a></li>'
        context += '</ul>'
    return JsonResponse({'context':context})
    return render(request, 'popup.html', {})

def beverage(request):
    return render(request, 'beverage.html')

# def view(request, path_end):
#     extensions = ['html', 'htm', 'zip', 'py', 'css', 'js', 'jpeg', 'jpg', 'png', 'pdf']
#     fm = FileManager( settings.MEDIA_ROOT, extensions=extensions)
#     return fm.render(request, path_end)


def filepicker(request):
    root_directory = 'P:\workspaces'
    return render(request, 'filepicker.html', {'rootdir':root_directory, })


def create_directory():
        command = ['qsub test.sge']
        try:
                process = Popen(command, stdout=PIPE, stderr=STDOUT)
                output = process.stdout.read()
                exitstatus = process.poll()
                if (exitstatus==0):
                        return {'status': 'Success', 'output':str(output)}
                else:
                        return {'status': 'Failed', 'output':str(output)}
        except Exception as e:
                return {'status': 'failed', 'output':str(e)}


def delete_directory():
        command = ['bash','multimodal/scripts/file_manipulater.sh','delete']
        try:
                process = Popen(command, stdout=PIPE, stderr=STDOUT)
                output = process.stdout.read()
                exitstatus = process.poll()
                if (exitstatus==0):
                        return {'status': 'Success', 'output':str(output)}
                else:
                        return {'status': 'Failed', 'output':str(output)}
        except Exception as e:
                return {'status': 'Failed', 'output':str(e)}


@csrf_exempt
def file_maniputer(request):
        if request.method == 'POST':
                request_data = ast.literal_eval(json.loads(request.body))
                if request_data['action'] == 'create':
                        data = create_directory()
                elif request_data['action'] == 'delete':
                        data = delete_directory()
                else:
                        data = {'status': 'not defined', 'output':'not defined'}
                response = HttpResponse(json.dumps(data), content_type='application/json', status=200)
                return response

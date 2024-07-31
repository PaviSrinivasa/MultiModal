import ast
import json
import logging
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


from .forms import WhisperForm, ClientFilePathField
from .models import Whisper
from django.conf import settings


@login_required(login_url='login')
def home(request):
    whiperInfo = Whisper.objects.all().order_by('-id')
    if request.method == 'GET':
        return render(request, 'home.html', {'whisperInfo':whiperInfo,})
    else:
        return render(request, 'home.html', {})


def whisper(request):
        if request.method == 'POST':
                filled_form = WhisperForm(request.POST, request.FILES)
                if filled_form.is_valid():
                    obj = filled_form.save(commit=False)
                    obj.submitter = request.user
                    filled_form.input_file_path = os.path.join(settings.MEDIA_ROOT,str(filled_form.cleaned_data['input_file_path']))
                    obj.input_file_path = filled_form.input_file_path
                    print(filled_form.input_file_path)
                    filled_form.save()
                    messages.success(request, 'Success!')
                else:
                        print(filled_form.errors)
                        messages.error(request, 'Failed!')
                new_form = WhisperForm()
                whiperInfo = Whisper.objects.all().order_by('-id')
                return render(request, 'home.html', {'whisperInfo':whiperInfo, })
        else:
                form = WhisperForm()
                return render(request, 'whisper.html', {'addform':form, })


# def file_browser(request):
#     root_directory = os.path.join('/mnt/d/work')
#     files = []
#     folders = []
#
#     if os.path.exists(root_directory):
#         if( root_directory[ len(root_directory) - 1 ] ==  '/' ):
#             folders = root_directory
#         else:
#             folders = root_directory+'/'
#         dir1 = dir(root_directory)
#         for f in os.walk(root_directory):
#             files.append(f)
#
#     if( len(files) > 2):  #First 2 entries are . and ..  -skip them
#         print(files)
#         files.sort()
#         print(files)
#         context = '<ul class="filetree" style="display: none;">'
#
#         for dirpath, dirs, f in os.walk(root_directory):
#             print(dirpath)
#             print (dirs)
#             print(f)
#             context += '<li class="folder collapsed"><a href="#" rel="'+ str(dirpath)+'/">' + str(dirs) + '</a></li>'
#             for file in f:
#                 ext = re.sub('/^.*\./', '', file)
#                 context += '<li class="file ext_'+ext+'"><a href="#" rel="' +dirpath+'">'+file+'</a></li>'
#         context += '</ul>'
#     return render(request, 'browser.html', {'context':context})


import ast
import json
from subprocess import Popen, PIPE, STDOUT

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .models import Whisper
from .forms import WhisperForm


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
        if request.method == 'POST':
                filled_form = WhisperForm(request.POST, request.FILES)
                if filled_form.is_valid():
                        obj = filled_form.save(commit=False)
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



# process = Popen(command, stdout=PIPE, stderr=STDOUT)
# output = process.stdout.read()
# exitstatus = process.poll()


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

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render,redirect
from django.http import Http404
from django.urls import NoReverseMatch
from django.contrib import messages

from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import json, requests
from subprocess import Popen, PIPE, STDOUT


@login_required(login_url='login')
def home(request):
    #expInfo = Info.objects.all().order_by('-id')
    if request.method == 'GET':
     #   myFilter = ExpFilter(request.GET, queryset=expInfo)
      #  expInfo = myFilter.qs
       # return render(request, 'home.html', {'expInfo': expInfo, 'myFilter': myFilter, })
        return render(request, 'home.html', {})
    else:
        return render(request, 'home.html', {})
        #return render(request, 'home.html', {'expInfo': expInfo, })


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
                request_data=json.loads(request.body)
                if request_data['action'] == 'create':
                        data = create_directory()
                elif request_data['action'] == 'delete':
                        data = delete_directory()
                else:
                        data = {'status': 'not defined', 'output':'not defined'}
                response = HttpResponse(json.dumps(data), content_type='application/json', status=200)
                return response

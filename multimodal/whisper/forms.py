from django import forms
from django.db import models

from .models import Whisper

class WhisperForm(forms.ModelForm):
    class Meta:
        model = Whisper
        fields = '__all__'
        labels = {
                    'name' : 'Name for this command run ',
                    'model': 'Model to use ',
                    'output_format': 'Format of the output file ',
                    'task' : 'Whether to perform speech recognition or translation ',
                    'language': 'Language spoken in the audio ',
                    'upload_file': 'Choose the file here '
        }

from django import forms
from django.db import models
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from .models import Whisper

from django.conf import settings, global_settings

filename= ' '



class FileNameInput(forms.widgets.FileInput):
    def render(self, name, value, attrs=None, renderer=None):
        html = super().render(name, value, attrs, renderer)
        if value:
            # Display the filename
            # html = f"<div>{value}</div>" + html
            html = format_html(
                "<div>{value}</div>{html}", value=mark_safe(value), html=mark_safe(html)
            )
        return html
class ClientFilePathField(forms.FileField):
    widget = FileNameInput

    def clean(self, data, initial=None):
        if data:
            # 'data' is an instance of InMemoryUploadedFile or TemporaryUploadedFile
            print(f"{data=}")
            print(f"{type(data)=}")
            print(f"{dir(data)=}")
            print(f"{vars(data)=}")
            filename = data.name
            print(f"{filename=}")
            return filename
        return initial

class WhisperForm(forms.ModelForm):
    input_file_path = ClientFilePathField()
    Whisper.input_file_path= str.join(str(settings.MEDIA_ROOT),filename) # trying to see if the value gets assigned here.

    class Meta:
        model = Whisper
        fields = '__all__'
        labels = {
                    'name': 'Name for this command run ',
                    'model': 'Model to use ',
                    'output_format': 'Format of the output file ',
                    'task': 'Whether to perform speech recognition or translation ',
                    'language': 'Language spoken in the audio ',
        }

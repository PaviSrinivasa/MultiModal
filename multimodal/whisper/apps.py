from django.apps import AppConfig



class WhisperConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'whisper'

    def ready(self):
        whisper = self.get_model('Whisper')

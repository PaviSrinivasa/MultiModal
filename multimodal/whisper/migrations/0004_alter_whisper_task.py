# Generated by Django 3.2.4 on 2023-03-29 10:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('whisper', '0003_whisper_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='whisper',
            name='task',
            field=models.CharField(choices=[('transcribe', 'transcribe'), ('Translate', 'translate')], max_length=10),
        ),
    ]
# Generated by Django 3.2.4 on 2023-04-24 09:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('whisper', '0006_whisper_submitter'),
    ]

    operations = [
        migrations.AddField(
            model_name='whisper',
            name='path',
            field=models.CharField(max_length=10000, null=True),
        ),
    ]

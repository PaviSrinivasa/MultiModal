# Generated by Django 3.2.4 on 2023-04-21 13:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('whisper', '0005_auto_20230403_1412'),
    ]

    operations = [
        migrations.AddField(
            model_name='whisper',
            name='submitter',
            field=models.CharField(blank=True, max_length=30),
        ),
    ]
# Generated by Django 3.0 on 2019-12-31 00:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EchoAnalyzer', '0007_auto_20191215_0238'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='processing_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='visit',
            name='processing_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]

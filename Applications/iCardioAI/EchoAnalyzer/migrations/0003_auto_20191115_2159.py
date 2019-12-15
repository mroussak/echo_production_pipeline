# Generated by Django 2.2.6 on 2019-11-15 21:59

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EchoAnalyzer', '0002_auto_20191114_2140'),
    ]

    operations = [
        migrations.AddField(
            model_name='visit',
            name='results',
            field=django.contrib.postgres.fields.jsonb.JSONField(null=True),
        ),
        migrations.AddField(
            model_name='visit',
            name='started_processing_at',
            field=models.DateTimeField(null=True),
        ),
    ]

# Generated by Django 2.2.5 on 2019-11-19 02:50

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0002_imagemodel'),
    ]

    operations = [
        migrations.AddField(
            model_name='questionrecord',
            name='comment',
            field=models.CharField(default='', max_length=500),
        ),
        migrations.AddField(
            model_name='questionrecord',
            name='correct_or_not',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.BooleanField(), default=[], size=None),
            preserve_default=False,
        ),
    ]

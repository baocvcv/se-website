# Generated by Django 2.2.5 on 2019-11-12 14:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0022_paperrecord_questionrecord'),
    ]

    operations = [
        migrations.AddField(
            model_name='paperrecord',
            name='need_judging',
            field=models.BooleanField(default=True),
        ),
    ]

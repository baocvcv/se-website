# Generated by Django 2.2.5 on 2019-10-22 03:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0004_auto_20191022_0310'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailverificationrecord',
            name='send_time',
            field=models.DateTimeField(verbose_name='Send time'),
        ),
    ]
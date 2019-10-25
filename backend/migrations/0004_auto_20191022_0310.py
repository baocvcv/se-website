# Generated by Django 2.2.5 on 2019-10-22 03:10

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0003_emailverificationrecord'),
    ]

    operations = [
        migrations.RenameField(
            model_name='emailverificationrecord',
            old_name='code',
            new_name='token',
        ),
        migrations.AlterField(
            model_name='emailverificationrecord',
            name='send_time',
            field=models.DateTimeField(default=datetime.datetime(2019, 10, 22, 3, 10, 24, 900609, tzinfo=utc), verbose_name='Send time'),
        ),
    ]

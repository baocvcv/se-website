# Generated by Django 2.2.5 on 2019-10-22 02:28

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0002_auto_20191018_0256'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmailVerificationRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=20, verbose_name='Code')),
                ('email', models.EmailField(max_length=50, verbose_name='Email')),
                ('send_type', models.CharField(choices=[('register', 'Register'), ('forget', 'Reset password')], max_length=10, verbose_name='Verification type')),
                ('send_time', models.DateTimeField(default=datetime.datetime(2019, 10, 22, 2, 28, 59, 70702, tzinfo=utc), verbose_name='Send time')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name': 'Email verification code',
                'verbose_name_plural': 'Email verification code',
            },
        ),
    ]
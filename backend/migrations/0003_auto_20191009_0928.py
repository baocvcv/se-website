# Generated by Django 2.2.5 on 2019-10-09 09:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0002_choiceq_multpchoiceq_question_singlechoiceq'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_admin',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='is_banned',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='is_superadmin',
            field=models.BooleanField(default=False),
        ),
    ]

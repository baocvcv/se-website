# Generated by Django 2.2.5 on 2019-11-18 10:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImageModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='pictures/')),
                ('date', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(blank=True, max_length=30, null=True)),
            ],
        ),
    ]

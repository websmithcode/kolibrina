# Generated by Django 3.0.7 on 2020-06-29 04:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('media', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='image',
            name='title',
        ),
    ]

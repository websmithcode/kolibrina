# Generated by Django 3.0.7 on 2020-06-29 05:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('media', '0002_remove_image_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='user',
            field=models.CharField(default='NullUserName', max_length=128),
        ),
        migrations.AlterField(
            model_name='image',
            name='image',
            field=models.ImageField(upload_to=models.CharField(default='NullUserName', max_length=128)),
        ),
    ]

# Generated by Django 3.0.7 on 2020-07-27 16:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userK', '0002_auto_20200708_0812'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='league',
            field=models.CharField(blank=True, choices=[('l1', 'Школьная лига'), ('l2', 'Лига колледжей'), ('l3', 'Студенческая лига'), ('l4', 'Высшая лига'), ('l5', 'Премьер-лига'), ('l6', 'Супер-лига')], max_length=2, verbose_name='Лига'),
        ),
    ]

# Generated by Django 4.2.7 on 2023-11-21 15:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Flow', '0014_rename_event_like_event_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='like',
            name='event_id',
            field=models.IntegerField(default=0),
        ),
    ]

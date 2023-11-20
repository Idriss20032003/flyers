# Generated by Django 4.2.7 on 2023-11-20 13:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Flow', '0008_alter_event_roadmap'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tags',
            name='event',
        ),
        migrations.AddField(
            model_name='tags',
            name='event',
            field=models.ManyToManyField(related_name='tag', to='Flow.event'),
        ),
    ]

# Generated by Django 4.2.7 on 2023-11-22 11:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Flow', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='event_type',
            field=models.CharField(choices=[('conference', 'Conférence'), ('workshop', 'Atelier'), ('meetup', 'Rencontre'), ('party', 'Soirée'), ('spectacle', 'Spectacle'), ('sport', 'Sport'), ('other', 'Autre')], default='other', max_length=20, null=True),
        ),
    ]

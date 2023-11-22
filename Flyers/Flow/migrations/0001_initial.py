# Generated by Django 4.2.7 on 2023-11-21 18:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.CharField(default='', max_length=500)),
                ('date', models.DateField(blank=True, null=True)),
                ('is_paid_event', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='', verbose_name='Illustration')),
                ('Roadmap', models.TextField(default='', null=True)),
                ('Likes', models.IntegerField(default=0)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='initiateur', to=settings.AUTH_USER_MODEL)),
                ('members', models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL)),
                ('money_man', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='money_man', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Tags',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('tag', models.CharField(max_length=20)),
                ('nb_events', models.PositiveIntegerField(default=0)),
                ('event', models.ManyToManyField(related_name='tag', to='Flow.event')),
                ('events', models.ManyToManyField(related_name='tags', to='Flow.event')),
            ],
        ),
    ]

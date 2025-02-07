from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Chat', '0002_delete_réponse_delete_sondage'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sondage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Reponse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('choix', models.CharField(max_length=100)),
                ('sondage', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reponses', to='Chat.sondage')),
            ],
        ),
    ]

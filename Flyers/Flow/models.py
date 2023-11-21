from django.db import models
from Authentication.models import User

class Event(models.Model):
    EVENT_TYPES = [
        	('conference', 'Conférence'),
            ('workshop', 'Atelier'),
            ('meetup', 'Rencontre'),
            ('party', 'Soirée'),
            ('spectacle', 'Spectacle'),
            ('sport', 'Sport'),
            ('other', 'Autre')
    ]

    title = models.CharField(max_length=100)
    description = models.CharField(max_length=500, default='')
    event_type = models.CharField(max_length=20, choices=EVENT_TYPES, default='other')
    date = models.DateField(null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='initiateur', null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(verbose_name='Illustration', null=True, blank=True)
    members = models.ManyToManyField(User, blank=True)
    Roadmap = models.TextField(default='', null=True)
    Likes = models.IntegerField(default=0)

class Tags(models.Model):
    tags = models.CharField(max_length=20)
    event = models.ManyToManyField(Event,  related_name= 'tags', blank = True)


# IL FAUT POUVOIR ACCEDER AU GROUPE DE DISCUSSION SSI ON FAIT PARTIE DE L'EVENT !

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

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
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='initiateur', null=True)
    is_paid_event = models.BooleanField(default=False)
    money_man = models.ForeignKey(User, on_delete=models.CASCADE, related_name='money_man', null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(verbose_name='Illustration', null=True, blank=True)
    image = models.ImageField(verbose_name='Illustration', null=True, blank=True, max_length=500)
    members = models.ManyToManyField(User, blank=True)
    Roadmap = models.TextField(default='', null=True)
    Likes = models.IntegerField(default=0, blank=True, null=True)

class Like(models.Model):
    event_id = models.IntegerField(default=0, blank=False, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Tags(models.Model):
    tags = models.CharField(max_length=20)
    event = models.ManyToManyField(Event,  related_name= 'tags', blank = True)


# IL FAUT POUVOIR ACCEDER AU GROUPE DE DISCUSSION SSI ON FAIT PARTIE DE L'EVENT !

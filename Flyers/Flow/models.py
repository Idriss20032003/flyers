from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from Authentication.models import Utilisateur


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
    ticket_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, null=True)
    money_man = models.ForeignKey(User, on_delete=models.CASCADE, related_name='money_man', null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(verbose_name='Illustration', null=True, blank=True)
    image = models.ImageField(verbose_name='Illustration', null=True, blank=True)
    members = models.ManyToManyField(User, blank=True)
    Roadmap = models.TextField(default='', null=True)
    Likes = models.IntegerField(default=0)

class Tags(models.Model):
    created_at = models.DateTimeField(default=timezone.now)
    tag = models.CharField(max_length=20)
    event = models.ManyToManyField(Event,  related_name= 'tag')
    events = models.ManyToManyField(Event, related_name='tags')
    nb_events = models.PositiveIntegerField(default=0)
    
class Reservation(models.Model):
    client = models.ForeignKey(Utilisateur, on_delete=models.SET_NULL, null=True, related_name='reservations')
    created_at = models.DateTimeField(default=timezone.now)
    is_paid = models.BooleanField(default=False)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

class TinyCart(models.Model):
    client = models.ForeignKey(Utilisateur, on_delete=models.SET_NULL, null=True, related_name='cart')
    created_at = models.DateTimeField(default=timezone.now)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)


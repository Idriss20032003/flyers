from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Event(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=500, default='')
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
    created_at = models.DateTimeField(default=timezone.now)
    tag = models.CharField(max_length=20)
    event = models.ManyToManyField(Event,  related_name= 'tag')
    events = models.ManyToManyField(Event, related_name='tags')
    nb_events = models.PositiveIntegerField(default=0)
    




# IL FAUT POUVOIR ACCEDER AU GROUPE DE DISCUSSION SSI ON FAIT PARTIE DE L'EVENT !

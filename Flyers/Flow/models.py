from django.db import models
from Authentication.models import User


class Event(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateField(null=True)
    created_by = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='initiateur', null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(
        verbose_name='Illustration', null=True, blank=True)
    members = models.ManyToManyField(User, blank=True)
    Roadmap = models.CharField(max_length=1000, default='')
    Likes = models.IntegerField(default=0)


class Tags(models.Model):
    tag = models.CharField(max_length=20)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)


# IL FAUT POUVOIR ACCEDER AU GROUPE DE DISCUSSION SSI ON FAIT PARTIE DE L'EVENT !

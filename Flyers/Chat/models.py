from django.db import models

from Authentication.models import User
from Flow.models import Event


class Message(models.Model):
    body = models.TextField()
    sent_by = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        User, blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        ordering = ('created_at',)

        def __str__(self):
            return f'{self.sent_by}'


class Room(models.Model):
    ACTIVE = 'active'
    CLOSED = 'closed'
    CHOICES_STATUS = (
        (CLOSED, 'closed'),
        (ACTIVE, 'active'),

    )

    name = models.CharField(max_length=255, blank=True, null=True)
    messages = models.ManyToManyField(Message, blank=True)
    url = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(
        max_length=20, choices=CHOICES_STATUS, default=CLOSED)
    created_at = models.DateTimeField(auto_now_add=True)
    event = models.OneToOneField(
        Event, on_delete=models.CASCADE, related_name='room', null=True)
    event_id = event.id

    class Meta:
        ordering = ('-created_at',)

        def __str__(self):
            return f'{self.uuid}'

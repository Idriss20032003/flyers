from Flow.models import *
from django import forms
from django.shortcuts import render


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        exclude = ('created_by', 'members', 'Likes', 'created_at')

class TagForm(forms.ModelForm):
    class Meta:
        model = Tags
        fields = ['tags']


EVENT_TYPES = (
	('', '-----'),
	('conference', 'Conférence'),
	('workshop', 'Atelier'),
    ('meetup', 'Rencontre'),
    ('party', 'Soirée'),
    ('spectacle', 'Spectacle'),
    ('sport', 'Sport'),
    ('other', 'Autre'),
    )

class SearchForm(forms.Form):
    
    title = forms.CharField(required = False)
    date = forms.DateField(required = False)
    event_type = forms.ChoiceField(widget = forms.Select, choices = EVENT_TYPES)
    tags = forms.CharField(required = False)

    
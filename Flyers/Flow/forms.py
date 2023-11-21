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
	('', 'Veuillez choisir parmi les choix'),
	('conference', 'Conférence'),
	('workshop', 'Atelier'),
    ('meetup', 'Rencontre'),
    ('party', 'Soirée'),
    ('spectacle', 'Spectacle'),
    ('sport', 'Sport'),
    ('other', 'Autre'),
    )

class SearchForm(forms.Form):
    #type = forms.ChoiceField(widget = forms.Select, choice = CHOICE)
    
    title = forms.CharField(required = False)
    date = forms.DateField(required = False)
    tags = forms.CharField(required = False)

    
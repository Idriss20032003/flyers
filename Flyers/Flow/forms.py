from Flow.models import *
from django import forms
from django.shortcuts import render


class EventForm(forms.ModelForm):
    tags = forms.CharField(required = False)

    class Meta:
        model = Event
        exclude = ('created_by', 'members', 'Likes', 'created_at')



CHOICE = (
	('', 'Veuillez choisir parmi les choix'),
	('0', 'Musique'),
	('1', 'Sport'),
    )

class SearchForm(forms.Form):
    #type = forms.ChoiceField(widget = forms.Select, choice = CHOICE)
    
    title = forms.CharField(required = False)
    date = forms.DateField(required = False)
    tags = forms.CharField(required = False)

    
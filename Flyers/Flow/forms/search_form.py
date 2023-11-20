from Flow.models import Event
from django import forms
from django.shortcuts import render

CHOICE = (
	('', 'Veuillez choisir parmi les choix><'),
	('0', 'mignonne'),
	('1', 'cool'),
	('2', 'passion'))

class TypeForm(forms.Form):
    select = forms.ChoiceField(widget = forms.Select, choice = CHOICE)
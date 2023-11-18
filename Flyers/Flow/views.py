from django.shortcuts import render
from .models import Event
# Create your views here.


def home(request):
    events = Event.objects.all()
    return render(request,
                  'Flow/home.html',
                  {'events': events})

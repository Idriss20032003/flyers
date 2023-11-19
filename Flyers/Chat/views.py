from django.shortcuts import render
import json

from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_GET
from .models import Room
from Flow.models import Event
# Create your views here.


def GroupPage(request):
    return render(request, 'Chat/GroupPage.html')


@require_POST
def create_room(request, event_id):
    event = Event.objects.get(id=event_id)
    name = f"groupe de : {event.title}"
    url = request.POST.get('url', '')
    Room.objects.create(name=name, event=event, url=url, event_id=event_id)
    return JsonResponse({'message': f"un groupe a été créé pour l'évènement {event.title}"})

# UUID = Event_id !!!!
# On créé une Room dès que l'on poste un évènement, l'id de l'évènement est alors intrinsèquement lié à la room
# On identifie alors la room avec event_id
# Chaque fois que qqn rejoint un évènement, on lui donne la permission de voir, dans son onglet "groupPage", et d'accéder, au chat du groupe correspondant.

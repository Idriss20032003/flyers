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
def create_room(request, event_id, uuid):
    name = request.POST.get('name', '')
    url = request.POST.get('url', '')
    event = Event.objects.get(id=event_id)
    created_by = event.created_by
    Room.objects.create(uuid=uuid, event=event, created_by=created_by, url=url)
    return JsonResponse({'message': f"un groupe pour l'évènement {event.title}"})

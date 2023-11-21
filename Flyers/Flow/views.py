from django.shortcuts import render
from .models import Event
from .forms import EventForm
from django.shortcuts import redirect
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
import json
from django.views.decorators.http import require_POST, require_GET

# Create your views here.


def home(request):
    events = Event.objects.all()
    return render(request,
                  'Flow/home.html',
                  {'events': events})


@login_required
def createEvent(request):
    if request.method == 'POST':
        # vérifier si on reçoit sous le bon format les données du formulaire html qui a été envoyé par l'api de JS
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.created_by = request.user
            event.save()
            event.members.add(request.user)
            # Réponse JSON indiquant que l'événement a été créé
            # A REMPLACER PLUS TARD PAR UN RENDER VERS LA PAGE SPECIFIQUE DE L'EVENT, CELA PERMETTRAIT AU JS DE RECUP L ID DE L'EVENT SPECIFIQUE
            ######################################
            print(event.id)
            return HttpResponse(json.dumps({'success': True, 'event_id': event.id}), content_type="application/json")

        else:
            # Envoie une erreur si les données ne sont pas valides
            # for field_name, field in form.fields.items():
            #    print(field_name, ':', field)
            return HttpResponse(json.dumps({'error': 'Invalid form data'}), status=400, content_type="application/json")

    else:
        form = EventForm()

    return render(request,
                  'Flow/create_event.html',
                  {'form': form})


@login_required
def joinEvent(request, eId):
    user = request.user
    event = Event.objects.get(id=eId)
    return render(request, 'Flow/joinEvent.html', {
        "eId": eId,
        "user": user,
        'event': event
    })


@login_required
def JoinEventConfirm(request, eId):
    user = request.user
    event = Event.objects.get(id=eId)
    event.members.add(user)
    return render(request, 'Flow/home.html', {
        "eId": eId,
        "user": user,
        'event': event
    })

from django.shortcuts import render
from .models import Event
from .forms import *
from django.shortcuts import redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

# Create your views here.


def home(request):
    events = Event.objects.all()

    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            #renvoie un dictionnaire des données du formulaire
            search_query = form.cleaned_data

            if search_query['tags']:
                results = Event.objects.filter(title__icontains=search_query['title'], date=search_query['date'], tag=search_query['tags'])
            else:
                results = Event.objects.filter(title__icontains=search_query['title'], date=search_query['date'])
            return render(request, 'Flow/search_result.html', {'form': form, 'results': results})
    form = SearchForm()

    return render(request,
                  'Flow/home.html',
                  {'events': events,'form': form})


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
            return JsonResponse({'success': True, 'event_id': event.id})

        else:
            # Envoie une erreur si les données ne sont pas valides
            for field_name, field in form.fields.items():
                print(field_name, ':', field)
            return JsonResponse({'error': 'Invalid form data'}, status=400)

    else:
        form = EventForm()

    return render(request,
                  'Flow/create_event.html',
                  {'form': form})


def search_form(request):

    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            #renvoie un dictionnaire des données du formulaire
            search_query = form.cleaned_data

            if search_query['tags']:
                results = Event.objects.filter(title__icontains=search_query['title'], date=search_query['date'], tag=search_query['tags'])
            else:
                results = Event.objects.filter(title__icontains=search_query['title'], date=search_query['date'])
            return render(request, 'Flow/search_result.html', {'form': form, 'results': results})
    form = SearchForm()

    return render(request, 'Flow/search.html', {'form': form})

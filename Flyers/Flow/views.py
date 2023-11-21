from django.shortcuts import render
from .models import Event
from .forms import *
from django.shortcuts import redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

# rendu de la page home
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

    list_events = serializers.serialize("json", Event.objects.all())

    return render(request,
                  'Flow/home.html',
                  {'events': events,'form': form, 'list_events': list_events})

# mise à jour du nombre de likes d'un event

@csrf_exempt  # Vous pouvez utiliser csrf_exempt si vous n'utilisez pas le jeton CSRF (à des fins de démonstration seulement)
@require_POST
def update_like(request):
    # Récupérez l'ID de l'élément à mettre à jour depuis la requête POST
    element_id = request.POST.get('element_id')

    # Mettez à jour la base de données (ajustez cette partie en fonction de votre modèle)
    votre_objet = Event.objects.get(id=element_id)
    votre_objet.Likes += 1
    votre_objet.save()

    # Retournez une réponse JSON
    #print(JsonResponse({'success': True, 'new_likes': votre_objet.Likes}))
    return JsonResponse({'success': True, 'new_likes': votre_objet.Likes})

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

from django.shortcuts import render
from .models import *
from .forms import *
from django.shortcuts import redirect
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
import json
from django.views.decorators.http import require_POST, require_GET

# rendu de la page home


def home(request):
    events = Event.objects.all().order_by('-created_at')
    form = SearchForm(request.GET)
    return render(request,'Flow/home.html', {'events': events, 'form': form})

def show_results(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            search_query = form.cleaned_data
            results = Event.objects.all()

            # Filtre par titre
            if search_query.get('title'):
                results = results.filter(title__icontains=search_query['title'])

            # Filtre par date
            if search_query.get('date'):
                results = results.filter(date=search_query['date'])

            # Filtre par tags
            if search_query.get('tags'):
                tags_list = ['#' + tag.strip() for tag in search_query['tags'].split('#') if tag.strip()]
                for tag in tags_list:
                    results = results.filter(tag__tag__contains=tag)

            # Filtre par type d'événement
            if search_query.get('event_type'):
                results = results.filter(event_type=search_query['event_type'])

            results = results.order_by('-created_at')
            return render(request, 'Flow/search_result.html', {'list_events': results})

    return redirect("home")

# mise à jour du nombre de likes d'un event

# Vous pouvez utiliser csrf_exempt si vous n'utilisez pas le jeton CSRF (à des fins de démonstration seulement)
@csrf_exempt
@require_POST
def update_like(request):
    # Récupérez l'ID de l'élément à mettre à jour depuis la requête POST
    element_id = request.POST.get('element_id')
    user = request.user

    # Vérifiez si l'utilisateur a déjà aimé le contenu
    if not Like.objects.filter(user=user, event_id=element_id).exists():
        # Ajoutez le "like" à la base de données
        objet_like = Like()
        objet_like.user = user
        objet_like.event_id = element_id
        objet_like.save()
        # Màj du champ "Likes" de Event

        votre_objet = Event.objects.get(id=element_id)
        votre_objet.Likes += 1
        votre_objet.save()

        # Réponse JSON indiquant le succès de la mise à jour
        return JsonResponse({'success': True, 'new_likes': votre_objet.Likes})

    # Réponse JSON indiquant que l'utilisateur a déjà aimé
    return JsonResponse({'success': False, 'new_likes': 0})


@login_required
def createEvent(request):
    if request.method == 'POST':
        # vérifier si on reçoit sous le bon format les données du formulaire html qui a été envoyé par l'api de JS
        event_form = EventForm(request.POST, request.FILES)
        tag_form = TagForm(request.POST)

        if event_form.is_valid() and tag_form.is_valid():
            # Sauvegarder l'objet Event sans les tags
            event = event_form.save(commit=False)
            event.created_by = request.user
            event.save()

            # Enregistrer les tags associés à l'événement
            tags_data = tag_form.cleaned_data.get('tag', '')
            tags_list = ['#' + tag.strip()
                         for tag in tags_data.split('#') if tag.strip()]

            for tag_text in tags_list:
                tag, created = Tags.objects.get_or_create(tag=tag_text)
                tag.save()
                event.tag.add(tag)

            event.members.add(request.user)

            try:
                # Sauvegarder à nouveau l'objet Event pour enregistrer les tags
                event.save()
            except Exception as e:
                print(f"Erreur d'enregistrement de l'event : {e}")

            # Réponse JSON indiquant que l'événement a été créé
            # A REMPLACER PLUS TARD PAR UN RENDER VERS LA PAGE SPECIFIQUE DE L'EVENT, CELA PERMETTRAIT AU JS DE RECUP L ID DE L'EVENT SPECIFIQUE
            ######################################
            print(event.id)
            return HttpResponse(json.dumps({'success': True, 'event_id': event.id}), content_type="application/json")

        else:
            # Envoie une erreur si les données ne sont pas valides
            for field_name, field in event_form.fields.items():
                print(field_name, ':', field)
            return JsonResponse({'error': 'Invalid form data'}, status=400)

    else:
        event_form = EventForm()
        tag_form = TagForm()

    return render(request,
                  'Flow/create_event.html',
                  {'event_form': event_form, 'tag_form': tag_form})


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
    events = Event.objects.all().order_by('-created_at')
    form = SearchForm(request.GET)
    return render(request, 'Flow/home.html', {
        "eId": eId,
        "user": user,
        'event': event,
        'events': events,
        'form': form
    })

def show_event(request, eId):
    event = Event.objects.get(id=eId)
    user_is_member = request.user in event.members.all()
    actual_nb_members = event.members.all().count() + 1
    return render(request, 'Flow/detail_event.html', {'event': event, 'user_is_member': user_is_member, 'actual_nb_members_plus_one': actual_nb_members})

def Roadmap_seeOnly(request, eId):
    event = Event.objects.get(id=eId)
    return render(request, 'Flow/roadmap_seeOnly.html', {'event': event})

def modify_event(request, eId):
    if request.user.is_authenticated:
        event = Event.objects.get(id=eId)
        if request.method == 'POST':
            form = EventModifyForm(request.POST, request.FILES, instance=event)
            print(form)
            if form.is_valid():
                form.save()
                return redirect('profile')
        else:
            form = EventModifyForm(instance=event)
        return render(request, 'Flow/modify_event.html', {'form': form, 'event': event})
    else:
        return redirect('login')
    
def leave_event(request, eId):
    if request.user.is_authenticated:
        event = Event.objects.get(id=eId)
        event.members.remove(request.user)
        return redirect('event', eId)
    else:
        return redirect('login')
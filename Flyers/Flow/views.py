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

# Create your views here.

# rendu de la page home
def home(request):
    empty_search = True
    events = Event.objects.all()
    form = SearchForm(request.GET)
    if request.method == "GET":
        if form.is_valid():
            #renvoie un dictionnaire des données du formulaire
            search_query = form.cleaned_data
            tags_list = ['#' + tag.strip() for tag in search_query['tag'].split('#') if tag.strip()]

            #test si une recherche a été faite
            for  value in search_query.values():
                if value not in ([], '', None):
                    empty_search = False
                    break
            
            if not empty_search :
                if search_query['tags']:
                    tags_list = ['#' + tag.strip() for tag in search_query['tag'].split('#') if tag.strip()]
                    results = Event.objects.filter(title__icontains=search_query['title'], 
                                                   date=search_query['date'],
                                                   event_type=search_query['event_type'], 
                                                   tags__tags__in=tags_list)
                else:
                    results = Event.objects.filter(title__icontains=search_query['title'], 
                                                   date=search_query['date'], 
                                                   event_type=search_query['event_type'])
                
                list_events = serializers.serialize("json", results)
                # Si des résultats sont trouvés, redirigez vers search_results.html
                return render(request, 'Flow/home.html', {'form': form, 'list_events': list_events})

    # Si aucune recherche n'a été effectuée ou si aucun résultat n'a été trouvé,
    # ou si la recherche a été effectuée avec succès, mais sans résultat, affichez home.html    
    form = SearchForm()
    list_events = serializers.serialize("json", events)
    empty_search = True

    return render(request,
                  'Flow/home.html',
                  {'events': events, 'form': form, 'list_events': list_events})



# mise à jour du nombre de likes d'un event

@csrf_exempt  # Vous pouvez utiliser csrf_exempt si vous n'utilisez pas le jeton CSRF (à des fins de démonstration seulement)
@require_POST
def update_like(request):
    # Récupérez l'ID de l'élément à mettre à jour depuis la requête POST
    element_id = request.POST.get('element_id')
    print("EFDZFSZFEZ " + element_id)
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
        event_form = EventForm(request.POST)
        tag_form = TagForm(request.POST)

        if event_form.is_valid() and tag_form.is_valid():
            # Sauvegarder l'objet Event sans les tags
            event = event_form.save(commit=False)
            event.created_by = request.user
            event.save()

            # Enregistrer les tags associés à l'événement
            tags_data = tag_form.cleaned_data.get('tags', '')
            tags_list = ['#' + tag.strip() for tag in tags_data.split('#') if tag.strip()]

            for tag_text in tags_list:
                tag, created = Tags.objects.get_or_create(tags=tag_text)
                tag.save()
                event.tags.add(tag)

            event.members.add(request.user)

            try :
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
    return render(request, 'Flow/home.html', {
        "eId": eId,
        "user": user,
        'event': event
    })


from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth.decorators import login_required
from .forms import *
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.views import LoginView
from Authentication.models import Utilisateur

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Utilisateur.objects.create(user=user, name=form.cleaned_data.get('pseudo'), email=user.username)  # Crée le profil client associé
            login(request, user)
            return redirect('profile')  # Rediriger vers la page d'accueil après l'inscription
    else:
        form = CustomUserCreationForm()
    return render(request, 'Authentication/signin.html', {'form': form})

class CustomLoginView(LoginView):
    form_class = CustomAuthenticationForm
    template_name = 'Authentication/login.html'



def show_profile(request):
    if request.user.is_authenticated:
        user = Utilisateur.objects.get(user=request.user)
        return render(request, 'Authentication/show_profile.html', {'user': user})
    else:
        return render(request, 'Authentication/signin.html')
    
def modify_profile(request):
    if request.user.is_authenticated:
        user = Utilisateur.objects.get(user=request.user)
        if request.method == 'POST':
            form = UtilisateurForm(request.POST, request.FILES, instance=user)
            print(form)
            if form.is_valid():
                form.save()
                return redirect('profile')
        else:
            form = UtilisateurForm(instance=user)
        return render(request, 'Authentication/modify_profile.html', {'form': form})
    else:
        return redirect('login')
    
def request_vendor_status(request):
    if request.method == 'POST':
        utilisateur = Utilisateur.objects.get(user=request.user)
        utilisateur.money_man_request_pending = True
        utilisateur.save()
        return redirect('profile')
    return redirect('home')

from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth.decorators import login_required
from .forms import *
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.views import LoginView

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Utilisateur.objects.create(user=user, name=form.cleaned_data.get('pseudo'), email=user.username)  # Crée le profil client associé
            login(request, user)
            return redirect('show_profile')  # Rediriger vers la page d'accueil après l'inscription
    else:
        form = CustomUserCreationForm()
    return render(request, 'Authentication/signin.html', {'form': form})

class CustomLoginView(LoginView):
    form_class = CustomAuthenticationForm
    template_name = 'Authentication/login.html'


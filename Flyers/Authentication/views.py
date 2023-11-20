
from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth.decorators import login_required

# Assurez-vous que le chemin de l'importation est correct
from .forms import LoginForm, SigninForm
# import des fonctions login et authenticate
from django.contrib.auth import login, authenticate, logout


def login_page(request):
    form = LoginForm()
    message = ''
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                message = f'Bonjour, {user.username}! Vous êtes connecté.'
                return redirect('home')
            else:
                message = 'Identifiants invalides.'
    return render(
        request, 'Authentication/login.html', context={'form': form, 'message': message})


@login_required
def logout_user(request):
    logout(request)
    return redirect('login')


def signin(request):
    form = SigninForm()
    if request.method == 'POST':
        form = SigninForm(request.POST)
        if form.is_valid():
            user = form.save()
            # auto-login user
            login(request, user)
            return redirect('home')

    return render(request, 'Authentication/signin.html', context={'form': form})

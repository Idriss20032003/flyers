from django.shortcuts import render
from Authentication.models import Utilisateur
# Create your views here.

def show_profile(request):
    if request.user.is_authenticated:
        user = Utilisateur.objects.get(user=request.user)
        return render(request, 'Profile/show_profile.html', {'user': user})
    else:
        return render(request, 'Authentication/signin.html')

#########################################################################################################################

# CHECKOUT ########################################################################################################

from . import views
from django.urls import path

urlpatterns = [
    path('', views.show_profile, name='show_profile'),
]


from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.urls import include, path
import Flow.views
import Authentication.views
import Chat.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Flow.views.home, name='home'),
    path('Groups/', Chat.views.GroupPage, name='GroupPage'),
    path('api/create-room/<int:eId>/',
         Chat.views.create_room, name='create-room'),
    path('create_event/', Flow.views.createEvent, name='create_event')

]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns

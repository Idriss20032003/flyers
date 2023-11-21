from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.urls import include, path
import Flow.views
import Authentication.views
import Chat.views
from django.contrib.auth.views import LogoutView
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Flow.views.home, name='home'),
    path('Search/', Flow.views.search_form, name = 'Search'),
    path('Groups/', Chat.views.GroupPage, name='GroupPage'),
    path('api/create-room/<int:eId>/',
         Chat.views.create_room, name='create-room'),
    path('create_event/', Flow.views.createEvent, name='create_event'),
    #path('login/', Authentication.views.login_page, name='login'),
    path('login/', Authentication.views.CustomLoginView.as_view(), name='login'),
    #path('logout/', Authentication.views.logout_user, name='logout'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('signin/', Authentication.views.register, name='signin'),
    path('GroupPage/', Chat.views.GroupPage, name='GroupPage'),
    path('profile/', include('Authentication.urls')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
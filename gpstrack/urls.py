from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView
from django.contrib.staticfiles.views import serve
from django.views.static import serve as media_serve

from django.conf import settings

from listenports.views import ListenPortView
from monitoring.views import IndexView, ProfileView, RegisterDoneView, RegisterUserView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('sendgps/', ListenPortView.as_view(), name = 'sendgps'),
    path('monitoring/', include('monitoring.urls')),
    path('ws/', include('websocket.urls')),
    path('', IndexView.as_view(), name = 'index'),
    path('accounts/login/', LoginView.as_view(next_page= 'monitoring'), name='login'),
    path('accounts/logout/', LogoutView.as_view(next_page= 'index'), name='logout'),
    path('accounts/register/done/', RegisterDoneView.as_view(), name='register_done'),
    path('accounts/register/', RegisterUserView.as_view(), name='register'),
    path('accounts/profile/', ProfileView.as_view(), name='profile'),
    path('accounts/password_change/', PasswordChangeView.as_view( 
        template_name='registration/change_password.html'), 
        name='password_change'),
    path('accounts/password_change/done/', PasswordChangeDoneView.as_view( 
        template_name= 'registration/password_changed.html'), 
        name='password_change_done'),
    path ('static/<path:path>', serve,{'insecure': True}),
    path('media/<path:path>', media_serve,{'document_root':settings.MEDIA_ROOT}),
]


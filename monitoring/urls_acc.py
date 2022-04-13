from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView
from monitoring.views import ProfileView, RegisterDoneView, RegisterUserView

urlpatterns = [
    path('login/', LoginView.as_view(next_page= 'monitoring'), name='login'),
    path('logout/', LogoutView.as_view(next_page= 'index'), name='logout'),
    path('register/done/', RegisterDoneView.as_view(), name='register_done'),
    path('register/', RegisterUserView.as_view(), name='register'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('password_change/', PasswordChangeView.as_view( 
        template_name='registration/change_password.html'), 
        name='password_change'),
    path('password_change/done/', PasswordChangeDoneView.as_view( 
        template_name= 'registration/password_changed.html'), 
        name='password_change_done'),
]

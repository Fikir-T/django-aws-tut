from .views import *
from django.urls import path
from django.contrib.auth import views as auth_views 
from .forms import LoginForm
# app_name = 'main'
urlpatterns = [
    path('', index , name='index'),
    path('aboutus',aboutus,name='aboutus'),
    path('signup/', signup , name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='main/login.html',authentication_form = LoginForm), name='login'),
    path('logout/',auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('profile/<int:pk>/', profile, name='profile'),
    path('success/', success,name='success'),
    path('filter_items/', filter_items, name='filter_items'),
    path('useractivity/',update_last_seen,name='useractivity'),
    path('visitors/',visitors,name='visitors'),
    path('visitorsreact/',visitors_json,name='visitorsreact'),
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name = 'main/reset_password.html') , name = 'reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name='main/reset_password_sent.html') , name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='main/reset_password_form.html'), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='main/reset_done.html'), name='password_reset_complete'),
]
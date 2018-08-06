from django.urls import path
from . import views

from django.contrib.auth import views as auth_views

urlpatterns = [
    path('accounts/login/', auth_views.login, {'template_name': 'auth/login.html'}, name='login'),
    path('accounts/logout/', auth_views.logout, {'next_page': '../login'}, name='logout'),
    path('error/', views.errorView, name='error'),
    path('account/creatuser', views.CreateUser, name='createuser'),
    path('account/changepw', views.ChangePassword, name='changepw')
]

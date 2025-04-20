from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),  # Usa la vista personalizada
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
    path('welcome/<int:user_id>/', views.welcome, name='welcome'),  # Cambia a `int:user_id`

]  
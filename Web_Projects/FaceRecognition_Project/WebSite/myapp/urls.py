from django.urls import path
from . import views

app_name = 'myapp'

urlpatterns = [
    path('', views.home, name='home'),
    path('registration/', views.register, name='register'),
    path('log_out/', views.log_out, name='log_out'),
    path('log_in/', views.log_in, name='log_in'),
    path('profile/<int:user_id>', views.profile, name='profile'),
    path('snapshot/', views.snapshot, name='snapshot'),
    path('reference/', views.reference, name='reference'),
    path('register_snapshot/', views.register_snapshot, name='register_snapshot'),
]

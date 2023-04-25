from django.urls import path
from core import views

app_name = 'core'

urlpatterns = [
    path("", views.home_view, name='index'),
    path("stage-one/", views.stage_one_view, name='stage_one_page'),
    path('stage-two/<str:q>/', views.stage_two_view, name='stage_two_page'),
    path('stage-three/', views.stage_three_view, name='stage_three_page'),
    path('result/', views.result_view, name='result_page'),
    path('success/', views.success_page_view, name='success_page'),
    path('fail/', views.fail_page_view, name='fail_page'),

    #About us
    path('about-us/', views.about_us_view, name='about_page'),
    path('contact/', views.contact_view, name='contact_page')
]
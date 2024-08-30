from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.prijava_view, name='prijava'),
    path('uspesna_prijava', views.uspesna_prijava, name='uspesna_prijava'),
    path('execute/', views.periodicno_view, name='execute'),
    path('atributi/', views.atributi_view, name='atributi'),
    path('', views.home_view, name='home'),
]
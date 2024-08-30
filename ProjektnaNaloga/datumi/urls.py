from django.urls import path
from . import views

urlpatterns = [
    path('termini/', views.termini_view, name='termini'),
]
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Termin


# Create your views here.

@login_required
def termini_view(request):
    uporabnik = request.user.uporabnik
    kategorija = uporabnik.kategorija
    lokacija = uporabnik.lokacija
    termini = Termin.objects.filter(kategorija=kategorija, lokacija=lokacija)
    return render(request, 'termini.html', {'termini': termini})
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import UporabnikRegistrationForm
from django.contrib.auth.decorators import login_required
import sys
from django.conf import settings

sys.path.append(settings.BASE_DIR)  ###da lahko import naredim iz parent directoryja

import periodicno
# Create your views here.

def prijava_view(request):  ###django view za prijavo, kjer si uporabnik izbere kategorijo in lokacijo
    if request.method == 'POST':
        form = UporabnikRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('uspesna_prijava')
    else:
        form = UporabnikRegistrationForm()
    return render(request, 'prijava.html', {'form': form})

@login_required
def uspesna_prijava(request):   ###samo redirect od prijave
    uporabnik = request.user.uporabnik
    kategorija = uporabnik.get_kategorija_display() ##da dobim verbose imena, ne tisto, kar je shranjeno v databazi, kot je na primer potrebno pri filtriranju za periodicno.py
    lokacija = uporabnik.get_lokacija_display()
    dict = {'kategorija': kategorija, 'lokacija': lokacija}
    return render(request, 'uspesna_prijava.html', dict)

@login_required
def atributi_view(request):     ###da vidi, kaj si je izbral, brez neke velike uporabnosti, narejen je bil za testiranje
    uporabnik = request.user.uporabnik
    kategorija = uporabnik.get_kategorija_display() ##da dobim verbose imena, ne tisto, kar je shranjeno v databazi, kot je na primer potrebno pri filtriranju za periodicno.py
    lokacija = uporabnik.get_lokacija_display()
    dict = {'kategorija': kategorija, 'lokacija': lokacija}
    return render(request, 'atributi.html', dict)

def periodicno_view(request):   ###zalaufa program
    if request.method == 'POST':
        periodicno.za_view()
        return render(request, 'run.html')
    return render(request, 'templates/run.html')

def home_view(request):         ###home view, z vsemi linki in tem
    return render(request, 'base.html')
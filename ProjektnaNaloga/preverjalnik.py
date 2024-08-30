import os
import django
from django.core.mail import send_mail


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ProjektnaNaloga.settings')
django.setup()

from userdata.models import Uporabnik

def obvesti(seznam):
    ###script ki posilja maile
    send_mail(
        'Novi termini',
        'Na voljo so novi izredni termini za Vašo izbiro kategorije in lokacije',
        'from@example.com',
        seznam,
        fail_silently=False
    )

def obvescevalec(kategorija, lokacija):
    ###script ki najde uporabnike in posle maile
    uporabniki = Uporabnik.objects.filter(kategorija=kategorija, lokacija=lokacija)
    maili = []
    for uporabnik in uporabniki:
        maili.append(uporabnik.user.email)

    obvesti(maili)
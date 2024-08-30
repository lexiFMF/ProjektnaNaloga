from scraper import main
from preverjalnik import obvescevalec
import django
import os
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ProjektnaNaloga.settings')
django.setup()

from datumi.models import Casovnica, Termin

kategorije = [4, 6, 14]
lokacije = [119, 221, 150, 185, 212]


def execute(kategorije_var, lokacije_var):
    for kategorija_var in kategorije_var:
        for lokacija_var in lokacije_var:
            ###skozi vse mozne kombinacije, trenutno hard coded
            main(kategorija_var, lokacija_var) #main()vrne timedelta, kar uporabim za oddaljenost termina
            prvi_termin = Termin.objects.filter(datum_in_cas__gte=timezone.now(), lokacija=lokacija_var, kategorija=kategorija_var).order_by('datum_in_cas').first()
            if prvi_termin:
                novo_stanje = (prvi_termin.datum_in_cas - timezone.now()).days
                casovnica = Casovnica.objects.filter(lokacija=lokacija_var, kategorija=kategorija_var).first()
                if casovnica:
                    timedelta = casovnica.timedelta
                    casovnica.delete()  ###izbrišem, saj bo ustvarjena nova
                else:
                    timedelta = 999
                nova_casovnica = Casovnica(kategorija=kategorija_var, lokacija=lokacija_var, timedelta=novo_stanje)
                nova_casovnica.save()
                if novo_stanje < timedelta: #ce je nov najblizji termin blizje kot prej, se poslje mail
                    obvescevalec(kategorija_var, lokacija_var)

                ###za demonstracijo, posle mail usakic ko zalaufa
                
def za_view():
    execute(kategorije, lokacije)


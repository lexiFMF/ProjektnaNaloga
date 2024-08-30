import requests
from bs4 import BeautifulSoup
import os
import django

#ne znam utemeljit, videl v tutorialu
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ProjektnaNaloga.settings')
django.setup()

from datumi.models import Termin

def scrape_termini(kategorija, lokacija):
    obmocje_slovar = {119:17, 221:18, 150:19, 185:20, 212:21}
    obmocje = obmocje_slovar[lokacija]
    url = f'https://e-uprava.gov.si/si/javne-evidence/prosti-termini/content/singleton.html?&type=1&cat={kategorija}&izpitniCenter={obmocje}&lokacija={lokacija}&offset=0&sentinel_type=ok&sentinel_status=ok&is_ajax=1'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    rezultati = soup.find_all('div', class_="js_dogodekBox dogodek top") + soup.find_all('div', class_="js_dogodekBox dogodek")
    tuples = []
    condensed = []
    st_ponovitev = []
    for rezultat in rezultati:
        datum = rezultat.find('div', class_="sr-only").text
        zacetek = rezultat.find_all('span', class_="bold")[-1].text
        tuples.append((datum, zacetek))
    for tuple in tuples:
        if tuple not in condensed:
            condensed.append(tuple)
            st_ponovitev.append(1)
        else:
            st_ponovitev[-1] += 1
    output = list(zip(condensed, st_ponovitev))
    return output

##make it execute periodically

def createtermin(datum_in_cas, lokacija, kategorija, st_mest):
    termin = Termin(datum_in_cas=datum_in_cas, lokacija=lokacija, kategorija=kategorija, st_mest=st_mest)
    termin.save()

def deletetermin(lokacija, kategorija):
    zrtve = Termin.objects.filter(lokacija=lokacija, kategorija=kategorija)
    zrtve.delete()

def main(kategorija, lokacija):
    deletetermin(lokacija, kategorija)
    output = scrape_termini(kategorija, lokacija)
    for tuple in output:
        dan, mesec, leto = tuple[0][0].split('. ')
        ura, minuta = tuple[0][1].split(':')
        datum_in_cas = f'{leto}-{mesec.zfill(2)}-{dan.zfill(2)} {ura.zfill(2)}:{minuta.zfill(2)}:00'
        st_mest = int(tuple[1])
        createtermin(datum_in_cas, lokacija, kategorija, st_mest)
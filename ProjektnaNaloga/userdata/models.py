from typing import Iterable
from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Uporabnik(models.Model):

###definiranje izbir za ta polja, na katera se sklicujejo atributi modela Uporabnik
    KATEGORIJA = (
        ('4', 'A'),
        ('6', 'B'),
        ('14', 'D'),
    )
    
    LOKACIJA = (
        ('119', 'KOPER'),   ###sam 1 iz vsazga obmocja za zdej
        ('221', 'LJUBLJANA'),
        ('150', 'CELJE'),
        ('185', 'NOVO MESTO'),
        ('212', 'MARIBOR')
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    kategorija = models.CharField(max_length=3, choices=KATEGORIJA)
    lokacija = models.CharField(max_length=9, choices=LOKACIJA)
    obmocje = models.IntegerField(max_length=2, blank=True)

    def save(self, *args, **kwargs):
        obmocje_slovar = {'119':17, '221':18, '150':19, '185':20, '212':21}
        self.obmocje = obmocje_slovar[self.lokacija]
        super().save(*args, **kwargs)

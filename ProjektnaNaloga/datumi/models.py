from django.db import models

# Create your models here.
class Termin(models.Model):

    KATEGORIJA = (
        ('4', 'A'),
        ('6', 'B'),
        ('14', 'D'),
    )

    LOKACIJA = (
        ('119', 'KOPER'),   ###bos pol na roko, muka zapopizdit, sam 1 iz vsazga obmocja za zdej
        ('221', 'LJUBLJANA'),
        ('150', 'CELJE'),
        ('185', 'NOVO MESTO'),
        ('212', 'MARIBOR')
    )
    datum_in_cas = models.DateTimeField(auto_now=False)
    lokacija = models.CharField(max_length=4, choices=LOKACIJA)
    kategorija = models.CharField(max_length=2, choices=KATEGORIJA)
    st_mest = models.IntegerField(max_length=2)

class Casovnica(models.Model):
    
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
    lokacija = models.CharField(max_length=4, choices=LOKACIJA)
    kategorija = models.CharField(max_length=2, choices=KATEGORIJA)
    timedelta = models.IntegerField(max_length=3, default=999)
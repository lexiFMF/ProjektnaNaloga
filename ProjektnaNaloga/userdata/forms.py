from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Uporabnik

class UporabnikRegistrationForm(UserCreationForm):
    kategorija = forms.ChoiceField(choices=Uporabnik.KATEGORIJA)
    lokacija = forms.ChoiceField(choices=Uporabnik.LOKACIJA)

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'email', 'kategorija', 'lokacija']

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            uporabnik = Uporabnik.objects.create(
                user=user,
                kategorija=self.cleaned_data['kategorija'],
                lokacija=self.cleaned_data['lokacija'],
            )
            uporabnik.save()
        return user
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


# formulaire d'inscription qui etend le formulaire de base de django
# j'ai ajoute le champ email en plus
class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=False, label="Email")

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

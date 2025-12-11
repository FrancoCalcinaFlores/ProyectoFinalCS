from django import forms
from .models import Consulta

class LoginForm(forms.Form):
    username = forms.CharField(label="Usuario")
    password = forms.CharField(label="Contraseña", widget=forms.PasswordInput)

class ConsultaForm(forms.ModelForm):
    class Meta:
        model = Consulta
        fields = ['mensaje']
        labels = {
            'mensaje': 'Mensaje para el administrador',
        }

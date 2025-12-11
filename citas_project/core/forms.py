from django import forms
from .models import Consulta
from .models import Cita

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
class CitaForm(forms.ModelForm):
    class Meta:
        model = Cita
        fields = ['doctor', 'fecha', 'hora', 'motivo']
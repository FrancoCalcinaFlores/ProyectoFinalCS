from django.db import models
from django.contrib.auth.models import User


class Paciente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    dni = models.CharField(max_length=20)
    telefono = models.CharField(max_length=20)

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name


class Cita(models.Model):
    # Paciente ahora es opcional: si está en blanco, la cita está disponible
    paciente = models.ForeignKey(
        Paciente,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    doctor = models.CharField(max_length=100)  # nuevo campo
    fecha = models.DateField()
    hora = models.TimeField()
    motivo = models.CharField(max_length=200)

    def __str__(self):
        if self.paciente:
            return f"{self.paciente} - Dr(a). {self.doctor} - {self.fecha} {self.hora}"
        return f"Cita disponible - Dr(a). {self.doctor} - {self.fecha} {self.hora}"


class Consulta(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    mensaje = models.TextField()
    fecha_envio = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(
        max_length=20,
        default="pendiente",
        choices=[
            ("pendiente", "Pendiente"),
            ("respondida", "Respondida")
        ]
    )

    def __str__(self):
        return f"Consulta de {self.paciente}"

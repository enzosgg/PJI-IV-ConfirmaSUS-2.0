from django.db import models
from django.contrib.auth.models import User


class Paciente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    cpf = models.CharField(max_length=11, unique=True)
    telefone = models.CharField(max_length=15)

    def __str__(self):
        return self.user.get_full_name()


class Medico(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    crm = models.CharField(max_length=11, unique=True)
    especialidade = models.CharField(max_length=50, null=True)
    consultorio = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.user.get_full_name()


class Consulta(models.Model):
    status = [
        ("consulta_disponivel", "Consulta disponível"),
        ("agendada", "Agendada"),
        ("na_unidade", "Na unidade"),
        ("compareceu", "Compareceu"),
        ("faltou", "Faltou"),
    ]
    status_retorno = [
        ("primeira_consulta", "Primeira Consulta"),
        ("retorno", "Paciente retornando"),
    ]
    paciente = models.ForeignKey(
        Paciente,
        on_delete=models.SET_NULL,
        related_name="consulta",
        null=True,
        blank=True,
    )
    medico = models.ForeignKey(
        Medico, on_delete=models.CASCADE, related_name="consulta"
    )
    data_hora = models.DateTimeField()
    local = models.CharField(max_length=255)
    endereco = models.CharField(max_length=255, blank=True, null=True)
    consulta_status = models.CharField(
        max_length=20, choices=status, default="consulta_disponivel"
    )
    consulta_status_retorno = models.CharField(
        max_length=20, choices=status_retorno, default="primeira_consulta"
    )

    class Meta:
        ordering = ["data_hora"]

    def __str__(self):
        return f" Consulta de Dr(a).{self.medico} em {self.data_hora.strftime('%d/%m/%Y às %H:%M')}"

    def save(self, *args, **kwargs):

        if self.paciente is None:
            self.consulta_status = "consulta_disponivel"

        elif self.consulta_status == "consulta_disponivel":
            self.consulta_status = "agendada"

        super().save(*args, **kwargs)

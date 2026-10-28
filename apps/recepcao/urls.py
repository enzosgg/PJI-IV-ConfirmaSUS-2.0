from django.urls import path
from . import views

urlpatterns = [
    path("", views.recepcao, name="recepcao"),
    path("login_paciente/", views.login_paciente, name="login_paciente"),
    path("login_medico/", views.login_medico, name="login_medico"),
    path("senha/", views.senha, name="senha"),
]

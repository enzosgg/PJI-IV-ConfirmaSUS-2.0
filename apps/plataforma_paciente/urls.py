from django.urls import path
from . import views

urlpatterns = [
    path("plataforma_paciente/", views.plataforma_paciente, name="plataforma_paciente"),
    path("consulta_interface/<int:id>/",views.consulta_interface,name="consulta_interface",),
    path("confirmar_presenca/<int:id>/",views.confirmar_presenca,name="confirmar_presenca",),path("cancelar_consulta/<int:id>/", views.cancelar_consulta, name="cancelar_consulta"),
    path("reagendar/<int:id>/", views.reagendar, name="reagendar"),
    path("confirmar-reagendamento/<int:id>/<int:novo_id>/",views.confirmar_reagendamento,name="confirmar_reagendamento",),
    path("marcar_consulta/", views.marcar_consulta, name="marcar_consulta"),
    path("confirmar_marcacao/<int:id>/",views.confirmar_marcacao,name="confirmar_marcacao"),
    path("perfil/", views.perfil, name="perfil"),
    path("logout/", views.logout, name="logout"),
]

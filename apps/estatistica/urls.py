from django.urls import path
from . import views

urlpatterns = [
    path("estatistica_interface/",views.estatistica_interface,name="estatistica_interface"),
    path("exportar_excel/", views.exportar_excel, name="exportar_excel"),
    path("powerbi_dados_mensais/",views.powerbi_dados_mensais,name="powerbi_dados_mensais"),
    path("powerbi_dados_totais/", views.powerbi_dados_totais, name="powerbi_dados_totais")
]

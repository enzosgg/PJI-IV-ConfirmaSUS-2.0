from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.recepcao.urls')),
    path('', include('apps.plataforma_paciente.urls')),
    path('', include('apps.plataforma_medico.urls')),
    path('', include('apps.estatistica.urls'))
]
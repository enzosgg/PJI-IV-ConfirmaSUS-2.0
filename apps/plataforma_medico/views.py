from django.shortcuts import render, redirect
from apps.cerebro.decorators import login_medico
from apps.cerebro.models import Consulta, Medico


@login_medico
def plataforma_medico(request):
    medico = Medico.objects.get(user=request.user)
    consulta = (
        Consulta.objects.filter(medico=medico, paciente__isnull=False)
        .select_related("paciente__user")
        .exclude(consulta_status="compareceu")
        .exclude(consulta_status="faltou")
    )
    return render(
        request, "plataforma_medico.html", {"medico": medico, "consulta": consulta}
    )


@login_medico
def consulta_medico(request, id):
    consulta = Consulta.objects.get(id=id, medico__user=request.user)
    return render(request, "consulta_medico.html", {"consulta": consulta})


@login_medico
def paciente_compareceu(request, id):
    consulta = Consulta.objects.get(id=id, medico__user=request.user)
    consulta.consulta_status = "compareceu"
    consulta.save()
    return redirect("plataforma_medico")


@login_medico
def paciente_faltou(request, id):
    consulta = Consulta.objects.get(id=id, medico__user=request.user)
    consulta.consulta_status = "faltou"
    consulta.save()
    return redirect("plataforma_medico")


@login_medico
def logout_medico(request):
    if "medico_id" in request.session:
        del request.session["medico_id"]
    return redirect("recepcao")

from django.shortcuts import render, redirect
from apps.cerebro.decorators import login_paciente
from apps.cerebro.models import Paciente, Consulta, Medico


@login_paciente
def plataforma_paciente(request):
    paciente = Paciente.objects.get(user=request.user)
    consulta = (
        Consulta.objects.filter(paciente=paciente)
        .exclude(consulta_status="compareceu")
        .exclude(consulta_status="faltou")
    )
    return render(
        request,
        "plataforma_paciente.html",
        {"paciente": paciente, "consulta": consulta},
    )


@login_paciente
def consulta_interface(request, id):
    consulta = Consulta.objects.get(id=id, paciente__user=request.user)
    return render(request, "consulta_interface.html", {"consulta": consulta})


@login_paciente
def confirmar_presenca(request, id):
    consulta = Consulta.objects.get(id=id, paciente__user=request.user)
    consulta.consulta_status = "na_unidade"
    consulta.save()
    return redirect("plataforma_paciente")


@login_paciente
def cancelar_consulta(request, id):
    consulta = Consulta.objects.get(id=id, paciente__user=request.user)
    consulta.paciente = None
    consulta.consulta_status = "consulta_disponivel"
    consulta.save()
    return redirect("plataforma_paciente")


@login_paciente
def reagendar(request, id):
    consulta = Consulta.objects.get(id=id, paciente__user=request.user)
    consulta_disponivel = Consulta.objects.filter(paciente__isnull=True)
    return render(
        request,
        "reagendar.html",
        {"consulta": consulta, "consulta_disponivel": consulta_disponivel},
    )


@login_paciente
def confirmar_reagendamento(request, id, novo_id):
    paciente = Paciente.objects.get(user=request.user)
    consulta = Consulta.objects.get(id=id, paciente__user=request.user)
    consulta_nova = Consulta.objects.get(id=novo_id, paciente__isnull=True)
    consulta.paciente = None
    consulta.consulta_status = "consulta_disponivel"
    consulta.save()
    consulta_nova.paciente = paciente
    consulta_nova.consulta_status = "agendada"
    consulta_nova.save()
    return redirect("plataforma_paciente")


@login_paciente
def marcar_consulta(request):
    paciente = Paciente.objects.get(user=request.user)
    especialidade = Medico.objects.values_list("especialidade", flat=True).distinct()
    especialidade_selecionada = request.GET.get("especialidade")
    consulta_disponivel = Consulta.objects.filter(paciente__isnull=True)

    if especialidade_selecionada:
        consulta_disponivel = consulta_disponivel.filter(
            medico__especialidade=especialidade_selecionada
        )

    return render(
        request,
        "marcar_consulta.html",
        {
            "paciente": paciente,
            "especialidade": especialidade,
            "consulta_disponivel": consulta_disponivel,
            "especialidade_selecionada": especialidade_selecionada,
        },
    )


@login_paciente
def confirmar_marcacao(request, id):
    paciente = Paciente.objects.get(user=request.user)
    consulta = Consulta.objects.get(id=id, paciente__isnull=True)
    consulta.paciente = paciente
    consulta.consulta_status = "agendada"
    consulta.save()
    return redirect("plataforma_paciente")


@login_paciente
def perfil(request):
    paciente = Paciente.objects.get(user=request.user)

    if request.method == "POST":
        paciente.telefone = request.POST.get("telefone")
        paciente.user.email = request.POST.get("email")
        paciente.save()
        paciente.user.save()
        return redirect("plataforma_paciente")

    return render(request, "perfil.html", {"paciente": paciente})


@login_paciente
def logout(request):
    if "paciente_id" in request.session:
        del request.session["paciente_id"]

    return redirect("recepcao")

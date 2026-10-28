from django.shortcuts import render, redirect
from apps.cerebro.models import Paciente, Medico
from django.contrib.auth import authenticate, login


def recepcao(request):
    return render(request, "recepcao.html")


def login_paciente(request):
    status = request.GET.get("status")

    if request.method == "POST":
        cpf = request.POST.get("cpf_sem_formatacao")
        senha = request.POST.get("senha")
        paciente = Paciente.objects.filter(cpf=cpf).first()
        paciente_autenticado = paciente and authenticate(
            request, username=paciente.user.username, password=senha
        )

        if paciente_autenticado:
            login(request, paciente_autenticado)
            request.session["paciente_id"] = paciente.id
            return redirect("plataforma_paciente")
        else:
            return redirect("/login_paciente/?status=1")

    return render(request, "login_paciente.html", {"status": status})


def login_medico(request):
    status = request.GET.get("status")

    if request.method == "POST":
        crm = request.POST.get("crm")
        senha = request.POST.get("senha")
        medico = Medico.objects.filter(crm=crm).first()
        medico_autenticado = medico and authenticate(
            request, username=medico.user.username, password=senha
        )

        if medico_autenticado:
            login(request, medico_autenticado)
            request.session["medico_id"] = medico.id
            return redirect("plataforma_medico")
        else:
            return redirect("/login_medico/?status=1")

    return render(request, "login_medico.html", {"status": status})


def senha(request):
    status = request.GET.get("status")

    if request.method == "POST":
        cpf = request.POST.get("cpf_sem_formatacao")
        paciente = Paciente.objects.filter(cpf=cpf).first()

        if paciente:
            return redirect("/senha/?status=2")
        else:
            return redirect("/senha/?status=1")

    return render(request, "senha.html", {"status": status})

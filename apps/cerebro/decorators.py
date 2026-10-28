from django.shortcuts import redirect


def login_paciente(view_func):

    def wrapper(request, *args, **kwargs):
        if "paciente_id" not in request.session:
            return redirect("recepcao")
        return view_func(request, *args, **kwargs)

    return wrapper


def login_medico(view_func):

    def wrapper(request, *args, **kwargs):
        if "medico_id" not in request.session:
            return redirect("recepcao")
        return view_func(request, *args, **kwargs)

    return wrapper

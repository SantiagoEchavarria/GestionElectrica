from django.shortcuts import redirect, render
from .models import Hogar, Dispositivo
from .forms import HogarForm, DispositivoForm

def registrar_hogar(request):
    if request.method=="POST":
        form= HogarForm(request.POST)
        if(form.is_valid):
            form.save()
            return redirect("lista_hogares")
    else:
        form = HogarForm
        return render(request, "registrar_hogar.html", {"form": form})

def registrar_dispositivos(request):
    if request.method == "POST":
        form = DispositivoForm(request.POST)
        if(form.is_valid):
            form.save()
            return redirect("lista_dispositivos")
    else:
        form=DispositivoForm()
        return render(request, "registrar_dispositivo.html", {"form": form})

def lista_hogares(request):
    hogares = Hogar.objects.all()
    return render(request, "lista_hogares.html", {"hogares": hogares})

def lista_dispositivos(request):
    dispositivos = Dispositivo.objects.all()
    return render(request, "lista_dispositivos.html", {"dispositvos": dispositivos})
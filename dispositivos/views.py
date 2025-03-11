from django.shortcuts import redirect, render
from .models import Hogar, Dispositivo, TipoDispositivo, ParteHogar
from .forms import HogarForm, DispositivoForm, TipoDispotivoForm, ParteHogarForm

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
    
def registrar_tipo_dispositivos(request):
    if request.method == "POST":
        form = TipoDispotivoForm(request.POST)
        if form.is_valid:
            form.save()
            return redirect("lista_tipos_dispositivos")
    else:
        form=TipoDispotivoForm()
        return render(request, "registrar_tipo_dispositivos.html", {"form":form})
    
def registrar_partes_hogar(request):
    if request.method=="POST":
        form = ParteHogarForm(request.POST)
        if form.is_valid:
            form.save()
            return redirect("listar_partes_hogar")
    else: 
        form=ParteHogarForm()
        return render(request, "registrar_partes_hogar.html", {"form": form})

def lista_hogares(request):
    hogares = Hogar.objects.all()
    return render(request, "lista_hogares.html", {"hogares": hogares})

def lista_dispositivos(request):
    dispositivos = Dispositivo.objects.all()
    return render(request, "lista_dispositivos.html", {"dispositvos": dispositivos})

def lista_tipos_dispositivos(request):
    tipoDispositivo = TipoDispositivo.objects.all()
    return render(request, "lista_tipos_dispositivos.html", {"tiposDispositivo":tipoDispositivo})

def listar_partes_hogar(request):
    partesHogar = ParteHogar.objects.all()
    return render (request, "listar_partes_hogar.html", {"partes": partesHogar}) 
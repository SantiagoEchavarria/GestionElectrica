from django.shortcuts import redirect, render
from .models import Hogar, Dispositivo, TipoDispositivo, ParteHogar
from .forms import HogarForm, DispositivoForm, TipoDispotivoForm, ParteHogarForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404
from .models import Dispositivo
from django.http import HttpResponseRedirect
from django.urls import reverse

#Hogares
@login_required                        
def registrar_hogar(request):
    if request.method=="POST":
        form= HogarForm(request.POST)
        if(form.is_valid):
            form.save()
            return redirect("lista_hogares")
    else:
        form = HogarForm
        return render(request, "registrar_hogar.html", {"form": form})
    
@login_required
def lista_hogares(request):
    hogares = Hogar.objects.all()
    return render(request, "lista_hogares.html", {"hogares": hogares})


#Partes de Hogar    
@login_required   
def registrar_partes_hogar(request):
    if request.method=="POST":
        form = ParteHogarForm(request.POST)
        if form.is_valid:
            form.save()
            return redirect("listar_partes_hogar")
    else: 
        form=ParteHogarForm()
        return render(request, "registrar_partes_hogar.html", {"form": form})
    
@login_required
def listar_partes_hogar(request):
    partesHogar = ParteHogar.objects.all()
    return render (request, "listar_partes_hogar.html", {"partes": partesHogar}) 

#Dispositivos
@login_required
def registrar_dispositivos(request):
    if request.method == "POST":
        form = DispositivoForm(request.POST)
        if(form.is_valid):
            form.save()
            return redirect("lista_dispositivos")
    else:
        form=DispositivoForm()
        return render(request, "registrar_dispositivo.html", {"form": form})
    
@login_required
def editar_dispositivo(request, dispositivo_id):
    dispositivo = get_object_or_404(Dispositivo, id=dispositivo_id)
    if request.method == "POST":
        form = DispositivoForm(request.POST, instance=dispositivo)
        if form.is_valid():
            form.save()
            return redirect("lista_dispositivos")
    else:
        form = DispositivoForm(instance=dispositivo)
    return render(request, "registrar_dispositivo.html", {
        "form": form,
        "edicion": True,
        "dispositivo": dispositivo
    })
    
@login_required
def eliminar_dispositivo(request, dispositivo_id):
    dispositivo = get_object_or_404(Dispositivo, id=dispositivo_id)
    if request.method == "POST":
        dispositivo.delete()
        return redirect("lista_dispositivos")
    return redirect("lista_dispositivos")


@login_required
def lista_dispositivos(request):
    dispositivos = Dispositivo.objects.all()
    return render(request, "lista_dispositivos.html", {"dispositivos": dispositivos})  


@login_required
def cambiar_estado_dispositivo(request, dispositivo_id):
    dispositivo = get_object_or_404(Dispositivo, id=dispositivo_id)
    dispositivo.estado = 'apagado' if dispositivo.estado == 'encendido' else 'encendido'
    dispositivo.save()
    return HttpResponseRedirect(reverse('lista_dispositivos'))


#Tipos de Dispositivos
@login_required   
def registrar_tipo_dispositivos(request):
    if request.method == "POST":
        form = TipoDispotivoForm(request.POST)
        if form.is_valid:
            form.save()
            return redirect("lista_tipos_dispositivos")
    else:
        form=TipoDispotivoForm()
        return render(request, "registrar_tipo_dispositivos.html", {"form":form})

@login_required
def lista_tipos_dispositivos(request):
    tipoDispositivo = TipoDispositivo.objects.all()
    return render(request, "lista_tipos_dispositivos.html", {"tiposDispositivo":tipoDispositivo})



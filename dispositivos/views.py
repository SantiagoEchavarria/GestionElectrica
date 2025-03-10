from django.shortcuts import redirect, render
from .models import Hogar
from .forms import HogarForm

def registrar_hogar(request):
    if request.method=="POST":
        form= HogarForm(request.POST)
        if(form.is_valid):
            form.save()
            return redirect("lista_hogares")
    else:
        form = HogarForm
        return render(request, "registrar_hogar.html", {"form": form})

def lista_hogares(request):
    hogares = Hogar.objects.all()
    return render(request, "lista_hogares.html", {"hogares": hogares})
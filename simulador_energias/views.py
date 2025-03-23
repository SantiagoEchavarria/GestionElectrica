from django.shortcuts import render

from simulador_energias.models import Consumo, RegistroConsumo
from .forms import ConsumoForm
from dispositivos.models import Dispositivo
from datetime import datetime

def calcular_consumo(request):
    dispositivos = Dispositivo.objects.all()
    matriz_consumo = []
    
    if request.method=="POST":
        fecha_inicio = request.POST.get("fecha_inicio")
        fecha_fin = request.POST.get("fecha_fin")
        dispositivo_id = request.POST.get("dispositivo")
        
        if fecha_inicio and fecha_fin and dispositivo_id:
            fecha_inicio = datetime.strptime(fecha_inicio, "%Y-%m-%d").date()
            fecha_fin = datetime.strptime(fecha_fin, "%Y-%m-%d").date()
            dispositivo = Dispositivo.objects.get(id=dispositivo_id)
            
            consumo = Consumo(fecha_inicio=fecha_inicio, fecha_fin=fecha_fin)
            consumo.save()  
            resultado = consumo.calcular_consumo(dispositivo.nombre)
            
            for fila in resultado:
                RegistroConsumo.objects.create(
                    consumo=consumo,
                    dispositivo=fila[0],
                    fecha=fila[1],
                    consumo_electrico=fila[2],
                    hora=fila[3],
                    duracion=fila[4]
                )
                matriz_consumo.append(fila)
                
            print(matriz_consumo)
    return render(request, "consumo.html", {"dispositivos": dispositivos, "matriz_consumo": matriz_consumo})

            
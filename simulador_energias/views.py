from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from simulador_energias.models import Consumo, RegistroConsumo
from .forms import ConsumoForm
from dispositivos.models import Dispositivo
from datetime import datetime
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
from .models import Consumo  # ajusta si tu modelo tiene otro nombre
from .utils import verificar_registros_superan_umbral_en_rango

@login_required
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


@api_view(['GET'])
def verificar_umbral(request, id):
    try:
        consumo_obj = Consumo.objects.get(id=id)
    except Consumo.DoesNotExist:
        return Response({'error': 'Consumo no encontrado'}, status=status.HTTP_404_NOT_FOUND)

    fecha_inicio = request.GET.get('inicio')
    fecha_fin = request.GET.get('fin')

    try:
        fecha_inicio = datetime.strptime(fecha_inicio, "%Y-%m-%d").date()
        fecha_fin = datetime.strptime(fecha_fin, "%Y-%m-%d").date()
    except (ValueError, TypeError):
        return Response({'error': 'Formato de fecha inválido. Use YYYY-MM-DD'}, status=status.HTTP_400_BAD_REQUEST)

    resultado = verificar_registros_superan_umbral_en_rango(consumo_obj, fecha_inicio, fecha_fin)

    return Response({'resultado': resultado}, status=status.HTTP_200_OK)

            
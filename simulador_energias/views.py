from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from simulador_energias.models import Consumo, RegistroConsumo
from .forms import ConsumoForm
from dispositivos.models import Dispositivo
from datetime import datetime
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .utils import verificar_registros_superan_umbral_en_rango
from django.contrib import messages


from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from simulador_energias.models import Consumo, RegistroConsumo
from dispositivos.models import Dispositivo

@login_required
def listar_consumos(request):
    consumos = Consumo.objects.filter(usuario=request.user).order_by('-fecha_inicio')

    alerta_modal = request.session.pop('alerta_modal', None)  # <- Recuperamos solo una vez

    return render(request, 'lista_consumos.html', {
        'consumos': consumos,
        'alerta_modal': alerta_modal
    })



@login_required
def eliminar_consumo(request, consumo_id):
    consumo = get_object_or_404(Consumo, id=consumo_id, usuario=request.user)

    if request.method == 'POST':
        consumo.delete()
        messages.success(request, f'El consumo del {consumo.fecha_inicio} al {consumo.fecha_fin} ha sido eliminado correctamente.')
        return redirect('listar_consumos')

    return render(request, 'confirmar_eliminar_consumo.html', {'consumo': consumo})


@login_required
def calcular_consumo(request):
    dispositivos = Dispositivo.objects.all()
    matriz_consumo = []

    if request.method == "POST":
        fecha_inicio_str = request.POST.get("fecha_inicio")
        fecha_fin_str = request.POST.get("fecha_fin")
        dispositivo_id = request.POST.get("dispositivo")

        if fecha_inicio_str and fecha_fin_str and dispositivo_id:
            try:
                fecha_inicio = datetime.strptime(fecha_inicio_str, "%Y-%m-%d").date()
                fecha_fin = datetime.strptime(fecha_fin_str, "%Y-%m-%d").date()
                dispositivo = Dispositivo.objects.get(id=dispositivo_id)

                consumo = Consumo(fecha_inicio=fecha_inicio, fecha_fin=fecha_fin, usuario=request.user)
                consumo.save()
                resultado = consumo.calcular_consumo(dispositivo.nombre)

                consumo_total = 0
                horas = {}

                for fila in resultado:
                    consumo_valor = float(fila[2])
                    hora = int(fila[3])
                    consumo_total += consumo_valor
                    horas[hora] = horas.get(hora, 0) + consumo_valor

                    RegistroConsumo.objects.create(
                        consumo=consumo,
                        dispositivo=fila[0],
                        fecha=fila[1],
                        consumo_electrico=consumo_valor,
                        hora=hora,
                        duracion=int(fila[4]),
                        registro_id=fila[5]
                    )
                    matriz_consumo.append(fila)

                consumo_min = float(dispositivo.tipo.rango_consumo_min)
                consumo_max = float(dispositivo.tipo.rango_consumo_max)
                hora_pico = max(horas, key=horas.get) if horas else None

                if consumo_total > consumo_max:
                    tipo = "alto"
                    mensaje = f"Consumo total {consumo_total:.2f} kWh EXCEDE el máximo permitido."
                elif consumo_total < consumo_min:
                    tipo = "bajo"
                    mensaje = f"Consumo total {consumo_total:.2f} kWh está por DEBAJO del mínimo esperado."
                else:
                    return redirect('listar_consumos')

                request.session['alerta_modal'] = {
                    "mensaje": mensaje,
                    "tipo": tipo,
                    "min": consumo_min,
                    "max": consumo_max,
                    "total": f"{consumo_total:.2f}",
                    "dispositivo": dispositivo.nombre,
                    "pico": hora_pico
                }

                return redirect('listar_consumos')

            except ValueError:
                pass
            except Dispositivo.DoesNotExist:
                pass

    return render(request, "consumo.html", {
        "dispositivos": dispositivos,
        "matriz_consumo": matriz_consumo
    })


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

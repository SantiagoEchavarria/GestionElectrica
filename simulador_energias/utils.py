from collections import defaultdict
from datetime import date

def verificar_registros_superan_umbral_en_rango(consumo_obj, fecha_inicio: date, fecha_fin: date):
    registros = consumo_obj.registros.filter(fecha__range=(fecha_inicio, fecha_fin))
    if not registros:
        return []

    # Calcular el umbral general de la simulación
    umbral = umbral_operativo(consumo_obj)

    # Agrupar consumo por fecha
    consumo_por_dia = defaultdict(float)
    for r in registros:
        consumo_por_dia[r.fecha] += r.consumo_electrico

    # Verificar qué días superan el umbral
    dias_superan_umbral = []
    for fecha, consumo in consumo_por_dia.items():
        if consumo > umbral:
            dias_superan_umbral.append({
                'fecha': fecha,
                'consumo': round(consumo, 3),
                'umbral': umbral,
                'supera': True
            })

    return dias_superan_umbral

def umbral_operativo(consumo_obj):
    registros = consumo_obj.registros.all()
    if not registros:
        return 0
    consumo_total = sum(r.consumo_electrico for r in registros)
    dias = (consumo_obj.fecha_fin - consumo_obj.fecha_inicio).days + 1
    promedio_diario = consumo_total / dias
    umbral = promedio_diario * 1.2  # por ejemplo, 20% por encima del promedio
    return round(umbral, 3)

from django.urls import path
from . import views

urlpatterns = [
    path('', views.vista_optimizacion, name='vista_optimizacion'),
    path('consumo/', views.consumo_actual, name='consumo_actual'),
]

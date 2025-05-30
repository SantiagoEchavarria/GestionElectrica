
from django.contrib import admin
from django.urls import path
from usuarios import views
from django.contrib.auth import views as auth_views
from dispositivos import views as views_dispositivos
from simulador_energias import views as views_simulador
from optimisacion import views as views_optimisacion
from django.urls import include

urlpatterns = [
    path('admin/', admin.site.urls),
    #urls de usuarios
    path('', views.inicio, name='inicio'),
    path('crear_seccion/', views.crearSeccion, name='crear_seccion'),
    path('iniciar_seccion/', views.iniciarSeccion, name='iniciar_seccion'),
    path('cerrar_seccion/', views.cerrarSeccion, name='cerrar_seccion'),
    path('editar_seccion/', views.editarSeccion, name='editar_seccion'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    
    #urls dispositivos
    path("hogares/", views_dispositivos.lista_hogares, name="lista_hogares"),
    path("hogares/registrar", views_dispositivos.registrar_hogar, name="registrar_hogar"),
    path("dispositivos/", views_dispositivos.lista_dispositivos, name="lista_dispositivos"),
    path("dispositivos/registrar", views_dispositivos.registrar_dispositivos, name="registrar_dispositivo"),
    path("dispositivos/editar/<int:dispositivo_id>/", views_dispositivos.editar_dispositivo, name="editar_dispositivo"),
    path('dispositivos/eliminar/<int:dispositivo_id>/', views_dispositivos.eliminar_dispositivo, name='eliminar_dispositivo'),
    path("tipos-dispositivos/", views_dispositivos.lista_tipos_dispositivos, name="lista_tipos_dispositivos"),
    path("tipos-dispositivos/registrar", views_dispositivos.registrar_tipo_dispositivos, name="registrar_tipo_dispositivos"),
    path("partes-hogar/", views_dispositivos.listar_partes_hogar, name="listar_partes_hogar"),
    path("partes-hogar/registrar/", views_dispositivos.registrar_partes_hogar, name="registrar_partes_hogar"),
    path("dispositivos/<int:dispositivo_id>/cambiar_estado/", views_dispositivos.cambiar_estado_dispositivo, name="cambiar_estado_dispositivo"),

    #optimizaccion 
    path("optimizacion/", include("optimisacion.urls")),
    path('api/consumo/<int:id>/verificar', views_simulador.verificar_umbral, name='verificar_umbral'),
    path('consumo/<uuid:registro_id>/', views_optimisacion.grafico_consumo_por_registro, name='grafico_consumo'),
    
    #urls simulador
    path("consumo/calcular_consumo/", views_simulador.calcular_consumo, name="calcular_consumo"),
    path("consumo/listar_consumos/", views_simulador.listar_consumos, name="listar_consumos"),
    path('consumo/eliminar/<uuid:consumo_id>/', views_simulador.eliminar_consumo, name='eliminar_consumo'),

]

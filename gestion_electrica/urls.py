
from django.contrib import admin
from django.urls import path
from usuarios import views
from django.contrib.auth import views as auth_views

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
    
]

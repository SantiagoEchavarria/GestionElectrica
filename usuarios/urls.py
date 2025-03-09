from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import registro, iniciar_sesion

urlpatterns = [
    path('registro/', registro, name='registro'),
    path('login/', iniciar_sesion, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]

from django.urls import path
from . import views

urlpatterns = [
    path('crearEnvio', views.EnvioCrear.as_view(), name='envio_crear'),   
    path('detalleSeguimiento', views.EnvioDetalle.as_view(), name='envio_detalle'),
    path('listaEnvio', views.EnvioLista.as_view(), name='envio_lista'),
    path('editEnvio/<int:pk>', views.EnvioActualizar.as_view(), name='envio_actualizar')
]
from django.urls import path

from . import views

urlpatterns = [
   path('carrito', views.VistaCarrito.as_view(), name='vercarrito'),
   path('historialusuario', views.VistaUsuarioHistorial.as_view(), name='historial_usuario'),
   path('view/<int:pk>', views.VistaHistorial.as_view(), name='historial_detalle'),
   path('<int:pk>/delete/', views.ItemBorrar.as_view(), name='Carrito_borrar'),
   path('finalizar_compra', views.AgregarHistorialCompras,name='finalizar_comprar'),
]
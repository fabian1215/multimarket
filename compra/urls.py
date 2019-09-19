from django.urls import path
from django.contrib.auth.decorators import login_required, permission_required
from . import views

urlpatterns = [
   path('carrito', login_required( views.VistaCarrito.as_view() ), name='vercarrito'),
   path('historialusuario',  login_required( views.VistaUsuarioHistorial.as_view() ), name='historial_usuario'),
   path('historial_administrador', views.VistaAdministradorHistorial.as_view(), name='historial_administrador'),
   path('view/<int:pk>', login_required( views.VistaHistorial.as_view() ), name='historial_detalle'),
   path('<int:pk>/delete/', views.ItemBorrar.as_view(), name='Carrito_borrar'),
   path('finalizar_compra', views.AgregarHistorialCompras,name='finalizar_comprar'),
   path('aumentar_cantidad/<int:item_id>', views.AumentaCantidad,name='aumentar_cantidad'),
   path('disminuir_cantidad/<int:item_id>', views.DisminuirCantidad,name='disminuir_cantidad'),
]
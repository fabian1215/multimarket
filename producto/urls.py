from django.urls import path

from . import views
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


urlpatterns = [
  #  path('lista', views.ProductoLista.as_view(), name='producto_lista'),
    path('view/<int:pk>', views.ProductoDetalle.as_view(), name='producto_detalle'),
    path('new', views.ProductoCrear.as_view(), name='producto_crear'),
    path('edit/<int:pk>',  views.ProductoActualizar.as_view(), name='producto_actualizar'),
    path('delete/<int:pk>', views.ProductoBorrar.as_view(), name='producto_borrar'),
    path('actualizar_categoria/<int:pk>', views.CategoriaActualizar.as_view(), name='categoria_actualizar'),
    path('ocultos', views.ProductosOcultos.as_view(), name='productos_ocultos'),
    path('crearcategoria', views.CategoriaCrear.as_view(), name='categoria_crear'),
    path('filtro/<category_name>', views.ProductoCategoria,name='producto_categoria'),
    path('busqueda/<buscado>', views.ProductoBusqueda,name='producto_busqueda'),
    path('agregar_ajax', views.AgregarProductoCarrito,name='agregar_carro'),
    path('acceso_denegado', views.AccesoDenegado,name='acceso_denegado'),
    path('acceso_denegado', views.AccesoDenegado,name='acceso_denegado'),
    
    path('calificarproducto/<int:product>',  login_required( views.CalificarProducto.as_view() ), name='calificar_producto'),
    path('listarcategorias',  views.CategoriaLista.as_view(), name='categoria_lista'),
    

]
from django.urls import path

from . import views



urlpatterns = [
  #  path('lista', views.ProductoLista.as_view(), name='producto_lista'),
    path('view/<int:pk>', views.ProductoDetalle.as_view(), name='producto_detalle'),
    path('new', views.ProductoCrear.as_view(), name='producto_crear'),
    path('edit/<int:pk>',  views.ProductoActualizar.as_view(), name='producto_actualizar'),
    path('delete/<int:pk>', views.ProductoBorrar.as_view(), name='producto_borrar'),
    path('actualizar/<int:pk>', views.ProductoActualizar.as_view(), name='producto_actualizar'),

    path('crearcategoria', views.CategoriaCrear.as_view(), name='categoria_crear'),
    path('filtro/<category_name>', views.ProductoCategoria,name='producto_categoria'),

   
    path('busqueda/<buscado>', views.ProductoBusqueda,name='producto_busqueda'),
    path('agregar_carrito/<int:product_id>', views.AgregarProductoCarrito,name='agregar_carro'),
    path('agregar_ajax', views.AgregarProductoCarrito2,name='agregar_carro2')

]
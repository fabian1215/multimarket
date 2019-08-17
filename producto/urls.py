from django.urls import path

from . import views



urlpatterns = [
    path('lista', views.ProductoLista.as_view(), name='producto_lista'),
    path('lista', views.ProductoLista.as_view(), name='producto_lista'),
    path('view/<int:pk>', views.ProductoDetalle.as_view(), name='producto_detalle'),
    path('new', views.ProductoCrear.as_view(), name='producto_crear'),
    path('edit/<int:pk>',  views.ProductoActualizar.as_view(), name='producto_actualizar'),
    path('delete/<int:pk>', views.ProductoBorrar.as_view(), name='producto_borrar'),

    path('crearcategoria', views.CategoriaCrear.as_view(), name='categoria_crear'),
    path('filtro/<category_name>', views.ProductoCategoria,name='producto_categoria')
]
from django.shortcuts import render
from django.views.generic import ListView, DetailView 
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from producto.models import Producto
from producto.models import *
from compra.models import *
from django.urls import reverse_lazy
from django.shortcuts import get_list_or_404, get_object_or_404
from django.db.models import Count,  Sum, Avg
import json
from django.http import HttpResponse
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from rest_framework import viewsets
from django.db.models import Q


class QueryCategorias(viewsets.ReadOnlyModelViewSet):

    def get_queryset(self):
        FitraProductosActivos = Categoria.objects.filter(producto__Estado='activo')
        CuentaCategorias = FitraProductosActivos.annotate(cuenta_categoria=Count('producto__Categoria')).order_by('-cuenta_categoria')
        ExcluirNulos = CuentaCategorias.exclude(producto__Categoria__isnull=True).exclude(producto__Categoria__Nombre__exact='')
        queryset = ExcluirNulos
        return queryset

class ProductoLista(ListView): 
    template_name = "ProductoListar.html"
    model = Producto
    context_object_name = 'productos'
    fields = '__all__'
    
    #query que se utilizara para ocultar los productos con el estado "desactivado" de los templates
    queryset = Producto.objects.filter(Estado='activo').order_by('-Cantidad')
   
    def get_context_data(self, **kwargs):
        
        kwargs['cantidadCategoria'] =  QueryCategorias().get_queryset
        return super(ProductoLista, self).get_context_data(**kwargs)


class CategoriaLista(UserPassesTestMixin, ListView): 
    template_name = "CategoriaListar.html"
    login_url= 'account_login'
    model = Categoria
    context_object_name = 'categorias'
    fields = '__all__'
    def test_func(self):
        return self.request.user.is_superuser

    def handle_no_permission(self):
        return redirect('acceso_denegado')  

class ProductosOcultos(UserPassesTestMixin,ListView): 
    template_name = "ProductosOcultos.html"
    model = Producto
    context_object_name = 'productos'
    fields = '__all__'
    
    #query que se utilizara para ocultar los productos con el estado "desactivado" de los templates
    queryset = Producto.objects.filter(Estado='inactivo')

    def test_func(self):
        return self.request.user.is_staff

    def handle_no_permission(self):
        return redirect('acceso_denegado')  

    def get_context_data(self, **kwargs):
        cantidadCategoria =  QueryCategorias().get_queryset
        kwargs['cantidadCategoria'] = cantidadCategoria
        return super(ProductosOcultos, self).get_context_data(**kwargs)




def ProductoCategoria(request, category_name):
    #category es utilizado para dar el nombre individual de la categoria en la vista
    category =  Categoria.objects.get(Nombre=category_name)
    news_list = Producto.objects.filter(Categoria=category,Estado='activo')
    cantidadCategoria = QueryCategorias().get_queryset
  
    return render(request, "ProductoCategoria.html", {
        'news_list': news_list,
        'category': category,
         'cantidadCategoria': cantidadCategoria
    })


def ProductoBusqueda(request, buscado):
    #lista_busqueda =   Producto.objects.filter(Nombre__icontains=buscado) | Producto.objects.filter(Categoria__Nombre__icontains=buscado) | Producto.objects.filter(Descripcion__icontains=buscado) 
    BusquedaNombre = Producto.objects.filter(Nombre__icontains=buscado)
    BusquedaCategoria = Producto.objects.filter(Categoria__Nombre__icontains=buscado)
    BusquedaDescripcion =  Producto.objects.filter(Descripcion__icontains=buscado) 
    lista_busqueda  = ( BusquedaNombre | BusquedaCategoria | BusquedaDescripcion ).exclude(Estado='inactivo')
    cantidadCategoria =  QueryCategorias().get_queryset
    return render(request, "ProductoBusqueda.html", {
        'lista_busqueda': lista_busqueda,
        'cantidadCategoria': cantidadCategoria
    })




class ProductoDetalle(DetailView): 
    template_name = "ProductoDetalle.html"
    model = Producto
    fields = '__all__'
    
    def get_context_data(self, **kwargs):

        kwargs['cantidadCategoria'] =  QueryCategorias().get_queryset
        id = self.kwargs['pk']
        productoSeleccionado =  Producto.objects.get(id=id)
        categoriaProducto= productoSeleccionado.Categoria
        ProductosMismaCategoria = Producto.objects.filter(Categoria=categoriaProducto)
        ExcluirNulos =  ProductosMismaCategoria.exclude(Categoria__Nombre__isnull=True).exclude(Categoria__Nombre__exact='').exclude(id=id)
        ProductosRelacionados = ExcluirNulos.order_by('?')[:4]
        kwargs['productosRelacionados'] = ProductosRelacionados
        ############################################### TELLEZ #################################
        if self.request.user.is_authenticated:
           consultaCalificado = CalificacionProducto.objects.filter( Q(usuario_calificador=self.request.user) & Q(calificado=True) & Q(producto=productoSeleccionado) )
        else:
            consultaCalificado = False
        if not consultaCalificado:
            habilitado = True       
        else:
            habilitado = False    
           
        numeroCalificaciones = CalificacionProducto.objects.filter(producto=productoSeleccionado).count()
        promedioCalificaciones = CalificacionProducto.objects.filter(producto=productoSeleccionado).aggregate(promedio = Avg('calificacion'))['promedio']
        
        if promedioCalificaciones is not None:
            porcentajeEstrellas = ( promedioCalificaciones * 100 )/5
            porcentajeEstrellas = int(porcentajeEstrellas)
        else:
            porcentajeEstrellas =0
   
        kwargs['habilitado'] = habilitado 
        kwargs['porcentajeEstrellas'] = porcentajeEstrellas
        kwargs['numeroCalificaciones'] = numeroCalificaciones

        return super(ProductoDetalle, self).get_context_data(**kwargs)

    #Tellez  Cambios #
    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(CalificarProducto, self).get_form_kwargs(
        *args, **kwargs)
        return kwargs

    def form_valid(self, form):
    
        form.instance.usuario_calificador = self.request.user
        productoSeleccionado = Producto.objects.get(pk=self.kwargs['product'])
        form.instance.producto = productoSeleccionado
        form.instance.calificado = True
        return super(CalificarProducto, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('producto_lista')

    ######################## TELLEZ  Cambios ####################


class ProductoCrear(UserPassesTestMixin,CreateView): 
    template_name = "ProductoCrear.html"
    model = Producto
    fields = '__all__'
    
    def test_func(self):
        return self.request.user.is_staff
    
    def handle_no_permission(self):
        return redirect('acceso_denegado')

    def get_success_url(self):
        return reverse_lazy('producto_detalle', kwargs={'pk' : self.object.pk})
    
    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(ProductoCrear, self).get_form_kwargs(
        *args, **kwargs)
        return kwargs

class CategoriaCrear(UserPassesTestMixin, CreateView): 
    template_name = "CategoriaCrear.html"
    model = Categoria
    fields = '__all__'

    def test_func(self):
        return self.request.user.is_superuser
    
    def handle_no_permission(self):
        return redirect('acceso_denegado')

    def get_success_url(self):
        return reverse_lazy('producto_lista')


class ProductoActualizar(UserPassesTestMixin,UpdateView): 
    template_name = "ProductoActualizar.html"
    model = Producto
    fields = '__all__'

    def test_func(self):
        return self.request.user.is_staff
    
    def handle_no_permission(self):
        return redirect('acceso_denegado')

    def get_success_url(self):
        return reverse_lazy('producto_detalle', kwargs={'pk' : self.object.pk})

class CategoriaActualizar(UserPassesTestMixin,UpdateView): 
    template_name = "CategoriaActualizar.html"
    model = Categoria
    fields = '__all__'
    
    def test_func(self):
        return self.request.user.is_staff
    
    def handle_no_permission(self):
        return redirect('acceso_denegado')

    def get_success_url(self):
        return reverse_lazy('producto_lista')



class ProductoBorrar(DeleteView): 
    model = Producto 
    fields = '__all__'



def AgregarProductoCarrito(request):
    product_id = request.POST.get('product_id')
    productoAgregado =  Producto.objects.get(id=product_id)
  
    if  request.user.is_authenticated:
        #Se comprueba si el usuario tiene un carrito creado
        if  Carrito.objects.filter(Usuario=request.user).exists():
            carritoAsociado = Carrito.objects.get(Usuario=request.user)

        #Si el usuario no tiene un carrito creado se le crea uno
        else:
            carritoAsociado=  Carrito(Usuario=request.user) 
            carritoAsociado.save()
        #aqui llamamos el carrito ya ha sido llamado por el primer condicional o guardado por el segundo
        carritoAsociado = Carrito.objects.get(Usuario=request.user)
        if ItemCarrito.objects.filter(producto=productoAgregado,carrito=carritoAsociado).exists():        
            return JsonResponse({'foo': 'este producto ya fue agregado a el carrito de compras anteriormente','repetido': 'si'})
        else:
            nuevoItemCarrito = ItemCarrito(producto=productoAgregado,carrito=carritoAsociado, Cantidad=1)
            nuevoItemCarrito.save()
            return JsonResponse({'foo': 'El producto fue agregado al carrito de compras', 'repetido': 'no'})
    else:
        print('No esta autenticado')
        return JsonResponse({'foo': 'Registrate o inicia sesión para agregar productos al carrito de compras', 'repetido': '', 'logueado': 'no'})
         





def AccesoDenegado(request):
    return render(request, "Permisos.html", {
    })
    

class CalificarProducto(CreateView): 
    template_name = "CalificacionCrear.html"
    model = CalificacionProducto
  
    
    fields = ['calificacion']

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(CalificarProducto, self).get_form_kwargs(
        *args, **kwargs)
        return kwargs

    def form_valid(self, form):
    
        form.instance.usuario_calificador = self.request.user
        productoSeleccionado = Producto.objects.get(pk=self.kwargs['product'])
        form.instance.producto = productoSeleccionado
        form.instance.calificado = True
        return super(CalificarProducto, self).form_valid(form)

    def get_success_url(self):
        Productoid = Producto.objects.get(pk=self.kwargs['product'])
        return reverse_lazy('producto_detalle', kwargs={'pk' : Productoid.id})

    
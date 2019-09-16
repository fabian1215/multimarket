from django.shortcuts import render
from django.views.generic import ListView, DetailView 
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from producto.models import Producto
from producto.models import *
from compra.models import *
from django.urls import reverse_lazy
from django.shortcuts import get_list_or_404, get_object_or_404
from django.db.models import Count
import json
from django.http import HttpResponse
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect

class ProductoLista(ListView): 
    template_name = "ProductoListar.html"
    model = Producto
    context_object_name = 'productos'
    fields = '__all__'
    
    #query que se utilizara para ocultar los productos con el estado "desactivado" de los templates
    queryset = Producto.objects.filter(Estado='activo')
   
    def get_context_data(self, **kwargs):
        
      
       # kwargs['categorias'] = Categoria.objects.exclude(producto__Categoria__isnull=True).exclude(producto__Categoria__Nombre__exact='')
        kwargs['cantidadCategoria'] = Categoria.objects.annotate(cuenta_categoria=Count('producto__Categoria')).order_by('-cuenta_categoria').exclude(producto__Categoria__isnull=True).exclude(producto__Categoria__Nombre__exact='')
        #.exclude(Producto__Categoria__exact='')
        # And so on for more models
        #cuenta.objects.all()
        #Categoria.objects.filter(Producto__nombre__in=[Producto]).annotate(amount_of_products=Count('Producto')).values('Nombre', 'amount_of_products')
        return super(ProductoLista, self).get_context_data(**kwargs)



class ProductosOcultos(ListView): 
    template_name = "ProductosOcultos.html"
    model = Producto
    context_object_name = 'productos'
    fields = '__all__'
    
    #query que se utilizara para ocultar los productos con el estado "desactivado" de los templates
    queryset = Producto.objects.filter(Estado='inactivo')
   
    def get_context_data(self, **kwargs):
        
      
       # kwargs['categorias'] = Categoria.objects.exclude(producto__Categoria__isnull=True).exclude(producto__Categoria__Nombre__exact='')
        kwargs['cantidadCategoria'] = Categoria.objects.annotate(cuenta_categoria=Count('producto__Categoria')).order_by('-cuenta_categoria').exclude(producto__Categoria__isnull=True).exclude(producto__Categoria__Nombre__exact='')
        #.exclude(Producto__Categoria__exact='')
        # And so on for more models
        #cuenta.objects.all()
        #Categoria.objects.filter(Producto__nombre__in=[Producto]).annotate(amount_of_products=Count('Producto')).values('Nombre', 'amount_of_products')
        return super(ProductosOcultos, self).get_context_data(**kwargs)




def ProductoCategoria(request, category_name):
    
    category =  Categoria.objects.get(Nombre=category_name)
    news_list = Producto.objects.filter(Categoria=category)
    cantidadCategoria = Categoria.objects.annotate(cuenta_categoria=Count('producto__Categoria')).order_by('-cuenta_categoria').exclude(producto__Categoria__isnull=True).exclude(producto__Categoria__Nombre__exact='')

    return render(request, "ProductoCategoria.html", {
        'news_list': news_list,
        'category': category,
         'cantidadCategoria': cantidadCategoria
    })


def ProductoBusqueda(request, buscado):
    
    #lista_busqueda = Producto.objects.filter(Nombre__icontains=buscado)
    lista_busqueda =   Producto.objects.filter(Nombre__icontains=buscado) | Producto.objects.filter(Categoria__Nombre__icontains=buscado) | Producto.objects.filter(Descripcion__icontains=buscado) 
    cantidadCategoria = Categoria.objects.annotate(cuenta_categoria=Count('producto__Categoria')).order_by('-cuenta_categoria').exclude(producto__Categoria__isnull=True).exclude(producto__Categoria__Nombre__exact='')
    return render(request, "ProductoBusqueda.html", {
        'lista_busqueda': lista_busqueda,
        'cantidadCategoria': cantidadCategoria
    })




class ProductoDetalle(DetailView): 
    template_name = "ProductoDetalle.html"
    model = Producto
    fields = '__all__'
    
    def get_context_data(self, **kwargs):

        # kwargs['categorias'] = Categoria.objects.exclude(producto__Categoria__isnull=True).exclude(producto__Categoria__Nombre__exact='')
        kwargs['cantidadCategoria'] = Categoria.objects.annotate(cuenta_categoria=Count('producto__Categoria')).order_by('-cuenta_categoria').exclude(producto__Categoria__isnull=True).exclude(producto__Categoria__Nombre__exact='')
        id = self.kwargs['pk']
        productoSeleccionado =  Producto.objects.get(id=id)
        categoriaProducto= productoSeleccionado.Categoria
        kwargs['productosRelacionados'] = Producto.objects.filter(Categoria=categoriaProducto).exclude(Categoria__Nombre__isnull=True).exclude(Categoria__Nombre__exact='').exclude(id=id).order_by('?')[:4]
        #.exclude(Producto__Categoria__exact='')
        # And so on for more models
        #cuenta.objects.all()
        #Categoria.objects.filter(Producto__nombre__in=[Producto]).annotate(amount_of_products=Count('Producto')).values('Nombre', 'amount_of_products')
        return super(ProductoDetalle, self).get_context_data(**kwargs)


class ProductoCrear(UserPassesTestMixin,CreateView): 
    template_name = "ProductoCrear.html"
    model = Producto
    fields = '__all__'
    
    def test_func(self):
        return self.request.user.is_staff
    
    def handle_no_permission(self):
        return redirect('acceso_denegado')

    def get_success_url(self):
      #  return reverse_lazy('producto_lista')
        return reverse_lazy('producto_detalle', kwargs={'pk' : self.object.pk})
    
    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(ProductoCrear, self).get_form_kwargs(
        *args, **kwargs)
        return kwargs

class CategoriaCrear(CreateView): 
    template_name = "CategoriaCrear.html"
    model = Categoria
    
    fields = '__all__'
    
    def get_success_url(self):
        return reverse_lazy('producto_lista')


class ProductoActualizar(UpdateView): 
    template_name = "ProductoActualizar.html"
    model = Producto
    fields = '__all__'

    def get_success_url(self):
        return reverse_lazy('producto_lista')


class ProductoBorrar(DeleteView): 
    model = Producto 
    fields = '__all__'


def AgregarProductoCarrito(request,product_id):
    
    productoAgregado =  Producto.objects.get(id=product_id)
    carritoAsociado = Carrito.objects.get(Usuario=request.user)
    if ItemCarrito.objects.filter(producto=productoAgregado).exists():
        
        return JsonResponse({'status': 'item duplicado', 'producto':productoAgregado.Nombre})
        
    else:
        nuevoItemCarrito = ItemCarrito(producto=productoAgregado,carrito=carritoAsociado, CantidadComprar=1)
        nuevoItemCarrito.save()
        return JsonResponse({'status': 'OK'})


def AgregarProductoCarrito2(request):
    product_id = request.POST.get('product_id')
    productoAgregado =  Producto.objects.get(id=product_id)
    #Se comprueba si el usuario tiene un carrito creado
    if  request.user.is_authenticated:
        print('Esta autenticado')
        if  Carrito.objects.filter(Usuario=request.user).exists():
            carritoAsociado = Carrito.objects.get(Usuario=request.user)
            print('entra al if')
        #Si el usuario no tiene un carrito creado se le crea uno
        else:
            #   Carrito.objects.filter(Usuario=request.user)
            print('entra al else')
            carritoAsociado=  Carrito(Usuario=request.user) 
            carritoAsociado.save()

        #aqui llamamos el carrito ya ha sido llamado por el primer condicional o guardado por el segundo
        carritoAsociado = Carrito.objects.get(Usuario=request.user)

        if ItemCarrito.objects.filter(producto=productoAgregado,carrito=carritoAsociado).exists():
            messages.info(request, 'Este producto ya se encuentra en tu carrito de compras, da clic en el icono del carrito para cambiar la cantidad o finalizar tu compra')
            #return JsonResponse({'status': 'item duplicado', 'producto':productoAgregado.Nombre, "message": "Este producto ya se encuentra en tu carrito de compras, da clic en el icono del carrito para cambiar la cantidad o finalizar tu compra"})
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
    

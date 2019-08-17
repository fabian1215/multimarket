from django.shortcuts import render
from django.views.generic import ListView, DetailView 
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from producto.models import Producto
from producto.models import *
from django.urls import reverse_lazy
from django.shortcuts import get_list_or_404, get_object_or_404
from django.db.models import Count


class ProductoLista(ListView): 
    template_name = "ProductoListar copy.html"
    model = Producto
    context_object_name = 'productos'
    fields = '__all__'

    def get_context_data(self, **kwargs):
    
        kwargs['categorias'] = Categoria.objects.all()
        # And so on for more models
        #cuenta.objects.all()
        #Categoria.objects.filter(Producto__nombre__in=[Producto]).annotate(amount_of_products=Count('Producto')).values('Nombre', 'amount_of_products')
        return super(ProductoLista, self).get_context_data(**kwargs)


class ProductoCategoria(ListView): 
    template_name = "ProductoCategoria.html"
    model = Producto
    context_object_name = 'categoria'
    fields = '__all__'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['productos'] = Producto.objects.all()
        return context

def ProductoCategoria(request, category_name):
    
    category =  Categoria.objects.get(Nombre=category_name)
    news_list = Producto.objects.filter(Categoria=category)


    return render(request, "ProductoCategoria.html", {
        'news_list': news_list,
        'category': category
    })



class ProductoDetalle(DetailView): 
    template_name = "ProductoDetalle.html"
    model = Producto
    fields = '__all__'
class ProductoCrear(CreateView): 
    template_name = "ProductoCrear.html"
    model = Producto
    
    fields = '__all__'
    
    def get_success_url(self):
        return reverse_lazy('producto_lista')


class CategoriaCrear(CreateView): 
    template_name = "CategoriaCrear.html"
    model = Categoria
    
    fields = '__all__'
    
    def get_success_url(self):
        return reverse_lazy('producto_lista')


class ProductoActualizar(UpdateView): 
    model = Producto
    fields = '__all__'
class ProductoBorrar(DeleteView): 
    model = Producto 
    fields = '__all__'
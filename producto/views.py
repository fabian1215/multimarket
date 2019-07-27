from django.shortcuts import render
from django.views.generic import ListView, DetailView 
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from producto.models import Producto
from django.urls import reverse_lazy

class ProductoLista(ListView): 
    template_name = "ProductoListar copy.html"
    model = Producto
    context_object_name = 'productos'
    fields = '__all__'
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


class ProductoActualizar(UpdateView): 
    model = Producto
    fields = '__all__'
class ProductoBorrar(DeleteView): 
    model = Producto 
    fields = '__all__'
from django.shortcuts import render
from django.views.generic import DetailView, ListView, DeleteView
from compra.models import Carrito, ItemCarrito
from producto.models import Producto
from django.urls import reverse_lazy
# Create your views here.


class VistaCarrito(ListView): 
    template_name = "Carrito.html"
    model = Carrito
    context_object_name = 'carrito'
    fields = '__all__'

    def get_context_data(self, **kwargs):
     #   Carro = Carrito.objects.all()
     #consulta que funciona
     #  Consulta = ItemCarrito.objects.filter(carrito__id=1)
     #  Consulta = ItemCarrito.objects.filter(carrito__Usuario=1)
     #consulta de prueba
        Consulta = ItemCarrito.objects.filter(carrito__Usuario=self.request.user)
        kwargs['listacompras'] = Consulta
        #kwargs['listacompras'] = Carrito.objects.filter(Usuario='1')
        return super(VistaCarrito, self).get_context_data(**kwargs)

class ItemBorrar(DeleteView):
    model = ItemCarrito
    success_url = reverse_lazy('vercarrito')
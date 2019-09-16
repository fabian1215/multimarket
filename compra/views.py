from django.shortcuts import render
from django.views.generic import DetailView, ListView
from compra.models import Carrito, ItemCarrito, ItemHistorial , FinalizarCompra
from producto.models import Producto
from django.urls import reverse_lazy
from django.views.generic.edit import DeleteView
from django.db.models import Avg, Count, Min, Sum
from django.http import HttpResponse
from django.http import JsonResponse
 
class ItemBorrar(DeleteView):
    model = ItemCarrito
    success_url = reverse_lazy('vercarrito')


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
        carritoAsociado = Carrito.objects.get(Usuario=self.request.user)
        Consulta = ItemCarrito.objects.filter(carrito__Usuario=self.request.user)
        SumaTotalPrecio= Consulta.aggregate(ResultadoSuma=Sum('producto__Precio'))
        kwargs['listacompras'] = Consulta
        kwargs['PrecioTotal'] = SumaTotalPrecio
        kwargs['idCarrito'] = carritoAsociado
        #kwargs['listacompras'] = Carrito.objects.filter(Usuario='1')
        return super(VistaCarrito, self).get_context_data(**kwargs)


       


def AgregarHistorialCompras(request):
    carritoAsociado = Carrito.objects.get(Usuario=request.user)
    listaproductos =  ItemCarrito.objects.filter(carrito__Usuario=request.user)
    SumaTotalPrecio= listaproductos.aggregate(ResultadoSuma=Sum('producto__Precio'))
    DatosFinalizarCompra = FinalizarCompra(ValorTotalPagado=5000, Usuario=request.user)
    DatosFinalizarCompra.save()
   
    for itemsolicitado in listaproductos:
    #DatosProducto = Producto.objects.get(pk=itemsolicitado.producto.id)

        nuevoItemHistorial = ItemHistorial(producto=itemsolicitado.producto,
        CantidadComprada=itemsolicitado.Cantidad, ValorUnitarioPagado=itemsolicitado.producto.Precio,Finalizar=DatosFinalizarCompra) 
        nuevoItemHistorial.save()
    #consulta que borra todos los items que se acaban de agregar en el historial de la compra
    ItemBorrar= ItemCarrito.objects.filter(carrito__Usuario=request.user).delete()

    return JsonResponse({'status': 'OK'})


class VistaUsuarioHistorial(ListView): 
    template_name = "UsuarioHistorial.html"
    model = FinalizarCompra
    fields = '__all__'
    
    def get_context_data(self, **kwargs):
        Consulta = FinalizarCompra.objects.filter(Usuario=self.request.user)
        kwargs['CompraporUsuario'] = Consulta
        #kwargs['listacompras'] = Carrito.objects.filter(Usuario='1')
        return super(VistaUsuarioHistorial, self).get_context_data(**kwargs)


class VistaHistorial(ListView): 
    template_name = "Historial.html"
    model = ItemHistorial
    fields = '__all__'



    def get_context_data(self, **kwargs):
    #   Carro = Carrito.objects.all()
    #consulta que funciona  Usuario=request.user
    #  Consulta = ItemCarrito.objects.filter(carrito__id=1)
    #  Consulta = ItemCarrito.objects.filter(carrito__Usuario=1)
    #consulta de prueba
        id= self.kwargs['pk']
        Consulta1 = ItemHistorial.objects.filter(Finalizar__id=id)
        Consulta2 = FinalizarCompra.objects.filter(Usuario=self.request.user)
        ConsultaFecha = FinalizarCompra.objects.filter(id=id)
        SumaTotalPrecio= Consulta1.aggregate(ResultadoSuma=Sum('producto__Precio'))
        kwargs['listahistorial'] = Consulta1
        kwargs['Finalizarcompra'] = ConsultaFecha
        kwargs['PrecioTotal'] = SumaTotalPrecio
        #kwargs['listacompras'] = Carrito.objects.filter(Usuario='1')
        return super(VistaHistorial, self).get_context_data(**kwargs)

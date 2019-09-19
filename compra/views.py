from django.shortcuts import render
from django.views.generic import DetailView, ListView
from compra.models import Carrito, ItemCarrito, ItemHistorial , FinalizarCompra
from producto.models import Producto
from django.urls import reverse_lazy
from django.views.generic.edit import DeleteView
from django.db.models import Avg, Count, Min, Sum
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import redirect
from django.db.models import Count, F, Value
from django.contrib import messages
from Adicionales.models import  Envio
from django.utils.crypto import get_random_string
from datetime import *
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

 
class ItemBorrar(DeleteView):
    model = ItemCarrito
    success_url = reverse_lazy('vercarrito')


class VistaCarrito(ListView): 
    template_name = "Carrito.html"
    model = Carrito
    context_object_name = 'carrito'
    fields = '__all__'

    def get_context_data(self, **kwargs):

        carritoAsociado = Carrito.objects.get(Usuario=self.request.user)
        Consulta = ItemCarrito.objects.filter(carrito__Usuario=self.request.user).annotate(valorUnidades=F('Cantidad') * F('producto__Precio')).order_by('-Cantidad')
        if not Consulta:
            disable=True       
        else:
            disable=False
                                                                 
        SumaTotalPrecio= Consulta.annotate(valorUnidades=F('Cantidad') * F('producto__Precio')).aggregate(ResultadoSuma=Sum('valorUnidades'))
        kwargs['listacompras'] = Consulta
        kwargs['PrecioTotal'] = SumaTotalPrecio
        kwargs['idCarrito'] = carritoAsociado
        kwargs['disable'] = disable

        return super(VistaCarrito, self).get_context_data(**kwargs)


       


def AgregarHistorialCompras(request):

    listaproductos =  ItemCarrito.objects.filter(carrito__Usuario=request.user)
    if  not listaproductos:
        return redirect('vercarrito')      
    else:
        SumaTotalPrecio= listaproductos.annotate(valorUnidades=F('Cantidad') * F('producto__Precio')).aggregate(ResultadoSuma=Sum('valorUnidades'))
       
        #Requerimiento tellez#
        Usuario = request.user
        codigoSeguimiento = get_random_string(length=10, allowed_chars='23456789ABCDEFGHJKLMNPQRSTUVWXYZ')
        fechaCompra = datetime.now()
        DatosEnvio = Envio( codigo_seguimiento=codigoSeguimiento , 
                            fecha_en_preparacion= fechaCompra,
                            usuario = Usuario)                          
        DatosEnvio.save()       
        DatosFinalizarCompra = FinalizarCompra(ValorTotalPagado=SumaTotalPrecio.get('ResultadoSuma'), Usuario=request.user, Envio=DatosEnvio)
        DatosFinalizarCompra.save()
        ##

        for itemsolicitado in listaproductos:

            nuevoItemHistorial = ItemHistorial(producto=itemsolicitado.producto,
            CantidadComprada=itemsolicitado.Cantidad, ValorUnitarioPagado=itemsolicitado.producto.Precio,Finalizar=DatosFinalizarCompra) 
            nuevoItemHistorial.save()
            ObjetoProducto = Producto.objects.get(pk=itemsolicitado.producto.id)
            CantidadProductoActual = ObjetoProducto.Cantidad
            ObjetoProducto.Cantidad =  CantidadProductoActual- itemsolicitado.Cantidad
            if  ObjetoProducto.Cantidad == 0:
                ObjetoProducto.Estado = 'inactivo'
            ObjetoProducto.save()
        #consulta que borra todos los items que se acaban de agregar en el historial de la compra
        ItemBorrar= ItemCarrito.objects.filter(carrito__Usuario=request.user).delete()
        messages.success(request,'Tu compra fue registrada con exito')
        return redirect('historial_usuario') 
    


def AumentaCantidad(request,item_id):

    #obtenemos el id del item carrito al cual le queremos cambiar la cantidad
    ItemSeleccionado = ItemCarrito.objects.get(id=item_id)
    CantidadInventario= ItemSeleccionado.producto.Cantidad 
    #if carritoObtenido.Cantidad > 0:
    # CantidadActual = int (ItemCarrito.Cantidad)
    CantidadActual =  ItemSeleccionado.Cantidad
    if CantidadInventario > CantidadActual:
        NuevaCantidad = CantidadActual + 1 
        ItemSeleccionado.Cantidad = NuevaCantidad
        ItemSeleccionado.save()  
    return redirect('vercarrito')

def DisminuirCantidad(request,item_id):

    #obtenemos el id del item carrito al cual le queremos cambiar la cantidad
    ItemSeleccionado = ItemCarrito.objects.get(id=item_id)
    
    # CantidadActual = int (ItemCarrito.Cantidad)
    CantidadActual =  ItemSeleccionado.Cantidad
    NuevaCantidad = CantidadActual - 1 
    ItemSeleccionado.Cantidad = NuevaCantidad
    if ItemSeleccionado.Cantidad >= 1:
       ItemSeleccionado.save()  
    
    return redirect('vercarrito')

class VistaUsuarioHistorial(ListView): 
    template_name = "UsuarioHistorial.html"
    model = FinalizarCompra
    fields = '__all__'
    
    def get_context_data(self, **kwargs):
        Consulta = FinalizarCompra.objects.filter(Usuario=self.request.user).order_by('-id')
        kwargs['CompraporUsuario'] = Consulta
        return super(VistaUsuarioHistorial, self).get_context_data(**kwargs)



class VistaAdministradorHistorial(UserPassesTestMixin,ListView): 
    template_name = "AdministradorHistorial.html"
    model = FinalizarCompra
    fields = '__all__'
    
    def get_context_data(self, **kwargs):
        Consulta = FinalizarCompra.objects.all().order_by('-id')
        kwargs['CompraporUsuario'] = Consulta
        return super(VistaAdministradorHistorial, self).get_context_data(**kwargs)
    
    def test_func(self):
        return self.request.user.is_staff

    def handle_no_permission(self):
        return redirect('acceso_denegado')  



class VistaHistorial(ListView): 
    template_name = "Historial.html"
    model = ItemHistorial
    fields = '__all__'

    def get_context_data(self, **kwargs):
        id= self.kwargs['pk']
        ItemsComprados = ItemHistorial.objects.filter(Finalizar__id=id).annotate(valorUnidades=F('CantidadComprada') * F('producto__Precio'))
   
        ConsultaFecha = FinalizarCompra.objects.filter(id=id)
        SumaTotalPrecio= FinalizarCompra.objects.get(id=id)

        kwargs['listahistorial'] = ItemsComprados
        kwargs['Finalizarcompra'] = ConsultaFecha
        kwargs['PrecioTotal'] = SumaTotalPrecio

        return super(VistaHistorial, self).get_context_data(**kwargs)

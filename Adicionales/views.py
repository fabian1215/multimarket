from django.shortcuts import render
from django.views.generic import ListView, TemplateView, CreateView, UpdateView
from django.urls import reverse_lazy
from Adicionales.models import *
from datetime import *

# Create your views here.


class EnvioCrear(CreateView): 
    template_name = "adicionales/envioCrear.html"
    model = Envio
    fields = ['estado']

    def get_success_url(self):
        return reverse_lazy('envio_lista')

    

class EnvioLista(ListView): 
    template_name = "adicionales/envioListar.html"
 
    model = Envio
    context_object_name = 'envios'
    fields = '__all__'


class EnvioActualizar(UpdateView):
    template_name = "adicionales/envioCrear.html"
    model = Envio  
    fields = ['estado']

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(EnvioActualizar, self).get_form_kwargs(
        *args, **kwargs)
        return kwargs

    def form_valid(self, form):
    
        if form.instance.estado == 'ENTREGADO':
            form.instance.fecha_entregado = datetime.now() 
        elif form.instance.estado == 'ENVIADO':
            form.instance.fecha_envio = datetime.now() 
      
        return super(EnvioActualizar, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('envio_lista')


class EnvioDetalle(TemplateView):
    template_name='adicionales/envioSeguimiento.html'
    model = Envio

    def post(self, request, *args, **kwargs):
        codigoSeguimiento = request.POST['codigo_seguimiento']
        envios = Envio.objects.get(codigo_seguimiento=codigoSeguimiento)
      
        return render(request, 'adicionales/envioSeguimiento.html' , {'envio':envios
        })


    
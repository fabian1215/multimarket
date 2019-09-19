from django.db import models
from django.utils.crypto import get_random_string
from producto.models import *
from compra.models import *
from django.utils import timezone



   # usuario = models.ForeignKey(User,on_delete=models.CASCADE, null=True)   

class Envio(models.Model):
  
    ESTADO_ENVIO_CHOICES = [

        ( 'ENVIADO' , 'Enviado' ),
        ( 'ENTREGADO' , 'Entregado' ),
    ]

    codigo_seguimiento= models.CharField(max_length=10, verbose_name='Codigo de Seguimiento' )
    estado= models.CharField(max_length=50,  choices = ESTADO_ENVIO_CHOICES, default = 'PREPARACION')
    fecha_en_preparacion = models.DateTimeField( verbose_name='Fecha en preparacion')
    fecha_envio = models.DateTimeField( verbose_name='Fecha de envio', null=True)
    fecha_entregado = models.DateTimeField( verbose_name='Fecha de entrega', null=True)
    usuario= models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    

    def __str__(self):
        return self.codigo_seguimiento

    

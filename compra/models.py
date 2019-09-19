from django.db import models
from django.contrib.auth.models import User
from producto.models import *
from Adicionales.models import *
# Create your models here.


class Carrito(models.Model):
    Usuario= models.ForeignKey(User, on_delete=models.CASCADE, null=True) 


class ItemCarrito(models.Model):
    producto= models.ForeignKey(Producto, on_delete=models.CASCADE, null=True)
    carrito= models.ForeignKey(Carrito, on_delete=models.CASCADE, null=True)
    Cantidad= models.PositiveIntegerField()

class FinalizarCompra(models.Model):
    ValorTotalPagado= models.PositiveIntegerField()
    Fechacompra = models.DateTimeField(null=True,auto_now=True)
    Usuario= models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    Envio = models.ForeignKey(Envio, on_delete=models.CASCADE, null=True)

class ItemHistorial(models.Model):
    producto= models.ForeignKey(Producto, on_delete=models.CASCADE, null=True)
    CantidadComprada= models.PositiveIntegerField()
    ValorUnitarioPagado = models.PositiveIntegerField()
    Finalizar= models.ForeignKey(FinalizarCompra, on_delete=models.CASCADE, null=True)
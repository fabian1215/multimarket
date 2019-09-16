from django.db import models
from django.contrib.auth.models import User
from producto.models import *
# Create your models here.


class Carrito(models.Model):
    Usuario= models.ForeignKey(User, on_delete=models.CASCADE, null=True) 
  #  Valor= models.PositiveIntegerField()
  # Fechacompra = models.DateTimeField(null=True)

class ItemCarrito(models.Model):
    producto= models.ForeignKey(Producto, on_delete=models.CASCADE, null=True)
    carrito= models.ForeignKey(Carrito, on_delete=models.CASCADE,  null=True)
    CantidadComprar= models.PositiveIntegerField()
    def __str__(self):
        return self.producto
   
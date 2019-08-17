from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse_lazy

class Categoria (models.Model):  
    Nombre= models.CharField(max_length=50)  
    Descripcion= models.CharField(max_length=254)
    def __str__(self):
        return self.Nombre
   

class Producto(models.Model):
    Nombre= models.CharField(max_length=50)
    Descripcion= models.CharField(max_length=254)
    imagen = models.ImageField(upload_to='Productos_imagenes/')
    Cantidad= models.PositiveIntegerField()
    Precio= models.PositiveIntegerField()
    Categoria = models.ForeignKey(Categoria, null=True, on_delete=models.SET_NULL)  
   # usuario = models.ForeignKey(User,on_delete=models.CASCADE, null=True)


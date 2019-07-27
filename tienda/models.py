from django.db import models

# Create your models here.
class Tienda(models.Model):
    Nombre= models.CharField(max_length=50)
    Descripcion= models.CharField(max_length=254)

     
   # usuario = models.ForeignKey(User,on_delete=models.CASCADE, null=True)

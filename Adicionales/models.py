from django.db import models

# Create your models here.
class Regalo(models.Model):
    id_regalo= models.IntegerField()
    Valor_regalo= models.IntegerField()
    imagen = models.FileField(upload_to='Regalo_imagenes/')
    Correo_Para= models.CharField(max_length=50)
    Nombre_De= models.CharField(max_length=50)
    Mensaje= models.CharField(max_length=200)
    Cantidad= models.IntegerField()
    FechaentregaR = models.DateTimeField()

   # usuario = models.ForeignKey(User,on_delete=models.CASCADE, null=True)   
class Envio (models.Model):
    Codigo_Seguimiento= models.IntegerField(primary_key=True)
    estado= models.CharField(max_length=50)
    fecha_envio = models.DateTimeField()
    fecha_entregado = models.DateTimeField()


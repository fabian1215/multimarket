from django.db import models

# Create your models here.

class Compra():
     id_compra= models.IntegerField()
     Fechacompra = models.DateTimeField()
     Comisiongen= models.IntegerField()
     Valor= models.IntegerField()


    
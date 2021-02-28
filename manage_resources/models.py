from django.db import models

# Create your models here.
class Usuarios(models.Model):
    name = models.CharField(max_length=30)
    lastname= models.CharField(max_length=30)
    address= models.CharField(max_length=200)
    phone=models.CharField(max_length=10)
    email=models.EmailField(max_length=30)
    password=models.CharField(max_length=255)
    admin = models.BooleanField(default=False)
    active=models.BooleanField(default=True)

class Productos(models.Model):
    name=models.CharField(max_length=60)
    section=models.CharField(max_length=30)
    price=models.FloatField()
    image_url=models.CharField(max_length=255)
    amount=models.IntegerField()
    stock=models.BooleanField(default=True)

class Carrito(models.Model):
    iduser=models.IntegerField()
    idproduct=models.IntegerField()
    amount=models.IntegerField()
    date=models.CharField(max_length=50)
    status=models.BooleanField(default=False)

class Compras(models.Model):
    iduser = models.IntegerField()
    totalprice=models.FloatField()
    date=models.CharField(max_length=30)
    hour=models.CharField(max_length=20)
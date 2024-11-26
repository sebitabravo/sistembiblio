from django.db import models
from django.conf import settings


class Editorial(models.Model):
    nombre = models.CharField(max_length=255, unique=True)


class Autor(models.Model):
    nombre = models.CharField(max_length=255)


class Producto(models.Model):
    TIPO_PRODUCTO = [
        ('libro', 'Libro'),
        ('revista', 'Revista'),
        ('enciclopedia', 'Enciclopedia'),
    ]
    tipo = models.CharField(max_length=20, choices=TIPO_PRODUCTO)
    titulo = models.CharField(max_length=255)
    editorial = models.ForeignKey(Editorial, on_delete=models.PROTECT)
    autores = models.ManyToManyField(Autor)
    descripcion = models.TextField(blank=True)


class Bodega(models.Model):
    nombre = models.CharField(max_length=255, unique=True)

    def productos_en_bodega(self):
        return MovimientoDetalle.objects.filter(movimiento__bodega_destino=self).values('producto', 'cantidad')


class Movimiento(models.Model):
    bodega_origen = models.ForeignKey(
        Bodega, on_delete=models.SET_NULL, null=True, related_name='movimientos_salida')
    bodega_destino = models.ForeignKey(
        Bodega, on_delete=models.SET_NULL, null=True, related_name='movimientos_entrada')
    productos = models.ManyToManyField(Producto, through='MovimientoDetalle')
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)


class MovimientoDetalle(models.Model):
    movimiento = models.ForeignKey(Movimiento, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()

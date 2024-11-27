from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError


# -----------------------------------
# Modelo Editorial
# -----------------------------------
class Editorial(models.Model):
    nombre = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.nombre


# -----------------------------------
# Modelo Autor
# -----------------------------------
class Autor(models.Model):
    nombre = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre


# -----------------------------------
# Modelo Producto
# -----------------------------------
class Producto(models.Model):
    TIPO_PRODUCTO = [
        ('libro', 'Libro'),
        ('revista', 'Revista'),
        ('enciclopedia', 'Enciclopedia'),
    ]
    tipo = models.CharField(max_length=20, choices=TIPO_PRODUCTO)
    titulo = models.CharField(max_length=255)
    editorial = models.ForeignKey('Editorial', on_delete=models.PROTECT)
    autores = models.ManyToManyField('Autor')
    descripcion = models.TextField(blank=True)
    bodega = models.ForeignKey(
        'Bodega', on_delete=models.SET_NULL, null=True, blank=True,
        related_name='productos'
    )
    cantidad = models.PositiveIntegerField(default=0)  # Nueva cantidad

    def __str__(self):
        return f"{self.titulo} ({self.cantidad})"

    class Meta:
        ordering = ['titulo']


# -----------------------------------
# Modelo Bodega
# -----------------------------------
class Bodega(models.Model):
    nombre = models.CharField(max_length=255, unique=True)

    def productos_en_bodega(self):
        """
        Retorna los productos con sus cantidades asociadas a esta bodega.
        """
        return MovimientoDetalle.objects.filter(
            movimiento__bodega_destino=self
        ).select_related('producto')

    def total_productos(self):
        """
        Retorna la cantidad total de productos almacenados en esta bodega.
        """
        return sum(
            detalle.cantidad for detalle in MovimientoDetalle.objects.filter(
                movimiento__bodega_destino=self
            )
        )

    def __str__(self):
        return self.nombre

    class Meta:
        ordering = ['nombre']


# -----------------------------------
# Modelo Movimiento
# -----------------------------------
class Movimiento(models.Model):
    bodega_origen = models.ForeignKey(
        Bodega, on_delete=models.SET_NULL, null=True, blank=True, related_name='movimientos_salida')
    bodega_destino = models.ForeignKey(
        Bodega, on_delete=models.SET_NULL, null=True, related_name='movimientos_entrada')
    productos = models.ManyToManyField(Producto, through='MovimientoDetalle')
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    codigo = models.CharField(max_length=10, unique=True, blank=True)

    def clean(self):
        """
        Valida que la bodega de origen y destino sean diferentes.
        """
        if self.bodega_origen and self.bodega_origen == self.bodega_destino:
            raise ValidationError(
                "La bodega de origen y destino no pueden ser la misma."
            )

    def save(self, *args, **kwargs):
        """
        Genera un código único para cada movimiento al guardarlo.
        """
        if not self.pk:  # Si el objeto no tiene un pk, lo guarda primero
            super().save(*args, **kwargs)
        if not self.codigo:  # Si no tiene un código, lo genera usando el pk
            self.codigo = f"MOV-{self.pk:05d}"  # Código único basado en el ID
            super().save(*args, **kwargs)  # Guarda nuevamente para actualizar el código

    def __str__(self):
        return f"Movimiento {self.codigo} de {self.bodega_origen} a {self.bodega_destino}"

    class Meta:
        ordering = ['-fecha']  # Últimos movimientos primero


# -----------------------------------
# Modelo MovimientoDetalle
# -----------------------------------


class MovimientoDetalle(models.Model):
    movimiento = models.ForeignKey('Movimiento', on_delete=models.CASCADE)
    producto = models.ForeignKey('Producto', on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()

    def clean(self):
        """
        Validaciones personalizadas para MovimientoDetalle.
        """
        if not self.movimiento_id:  # Validar si ya tiene un movimiento asociado
            return  # No realizar validaciones si no está asignado todavía

        if self.movimiento.bodega_origen:
            # Verificar si el producto está en la bodega de origen
            if self.producto.bodega != self.movimiento.bodega_origen:
                raise ValidationError(
                    f"El producto '{self.producto.titulo}' no está en la bodega de origen '{self.movimiento.bodega_origen}'."
                )

            # Verificar disponibilidad de stock
            stock_disponible = self.producto.cantidad_disponible_en_bodega(
                self.movimiento.bodega_origen)
            if self.cantidad > stock_disponible:
                raise ValidationError(
                    f"No hay suficiente stock de '{self.producto.titulo}'. Disponible: {stock_disponible}."
                )

    def save(self, *args, **kwargs):
        """
        Actualiza el stock al guardar un detalle de movimiento.
        """
        if not self.pk:  # Si es una creación
            if self.movimiento.bodega_origen:
                self.producto.actualizar_stock(
                    self.movimiento.bodega_origen, -self.cantidad)
            if self.movimiento.bodega_destino:
                self.producto.actualizar_stock(
                    self.movimiento.bodega_destino, self.cantidad)
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """
        Revertir el stock si se elimina el movimiento.
        """
        if self.movimiento.bodega_origen:
            self.producto.actualizar_stock(
                self.movimiento.bodega_origen, self.cantidad)
        if self.movimiento.bodega_destino:
            self.producto.actualizar_stock(
                self.movimiento.bodega_destino, -self.cantidad)
        super().delete(*args, **kwargs)

    def __str__(self):
        return f"{self.cantidad} de {self.producto.titulo} en movimiento {self.movimiento.codigo}"

    class Meta:
        ordering = ['movimiento', 'producto']


# -----------------------------------
# Modelo Usuario
# -----------------------------------
class Usuario(AbstractUser):
    is_jefe_bodega = models.BooleanField(default=False)
    is_bodeguero = models.BooleanField(default=False)

    def clean(self):
        """
        Valida que un usuario no pueda tener ambos roles: jefe de bodega y bodeguero.
        """
        if self.is_jefe_bodega and self.is_bodeguero:
            raise ValidationError(
                "Un usuario no puede ser tanto jefe de bodega como bodeguero."
            )

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"

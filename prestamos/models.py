from django.db import models
from django.contrib.auth.models import User

class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre


class Herramienta(models.Model):
    ESTADO_HERRAMIENTA_CHOICES = [
        ('Bueno', 'Bueno'),
        ('Regular', 'Regular'),
        ('En reparación', 'En reparación'),
    ]

    codigo = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=100)
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT)
    estado = models.CharField(max_length=20, choices=ESTADO_HERRAMIENTA_CHOICES, default='Bueno')
    disponible = models.BooleanField(default=True)
    fecha_ingreso = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"


class Prestamo(models.Model):
    ESTADO_PRESTAMO_CHOICES = [
        ('Pendiente', 'Pendiente'),
        ('Activo', 'Activo'),
        ('Devuelto', 'Devuelto'),
        ('Cancelado', 'Cancelado'),
    ]

    socio = models.ForeignKey(User, on_delete=models.CASCADE)
    herramienta = models.ForeignKey(Herramienta, on_delete=models.CASCADE)
    fecha_solicitud = models.DateTimeField(auto_now_add=True)
    fecha_devolucion_esperada = models.DateField()
    fecha_devolucion_real = models.DateField(blank=True, null=True)
    estado = models.CharField(max_length=20, choices=ESTADO_PRESTAMO_CHOICES, default='Pendiente')

    def __str__(self):
        return f"Préstamo de {self.herramienta.nombre} a {self.socio.username}"
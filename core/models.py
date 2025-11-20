from django.db import models
from django.contrib.auth.models import User


class Role(models.Model):
    """Representa un rol de acceso por módulo o global."""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    roles = models.ManyToManyField(Role, blank=True)

    def __str__(self):
        return f"Profile: {self.user.username}"


class Person(models.Model):
    """Clase base abstracta para personas (docentes, alumnos, etc.).

    Provee campos comunes: nombre, apellido y DNI. Se usa como base para
    `Student` y `Teacher` para evitar duplicación.
    """
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    dni = models.CharField(max_length=20, blank=True)
    # Dirección
    street = models.CharField('calle', max_length=200, blank=True)
    street_number = models.CharField('número', max_length=20, blank=True)
    between_streets = models.CharField('entre calles', max_length=200, blank=True)
    locality = models.CharField('localidad', max_length=100, blank=True)
    postal_code = models.CharField('código postal', max_length=20, blank=True)
    # Teléfonos
    phone_primary = models.CharField('teléfono principal', max_length=50, blank=True)
    phone_secondary = models.CharField('teléfono secundario', max_length=50, blank=True)

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.last_name}, {self.first_name}"

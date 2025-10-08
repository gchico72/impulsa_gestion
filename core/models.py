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

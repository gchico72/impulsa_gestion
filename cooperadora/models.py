from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import date


class Transaction(models.Model):
    INCOME = 'IN'
    EXPENSE = 'EX'
    ADJUSTMENT = 'AJ'
    TYPE_CHOICES = [
        (INCOME, 'Ingreso'),
        (EXPENSE, 'Egreso'),
        (ADJUSTMENT, 'Ajuste'),
    ]

    date = models.DateField()
    type = models.CharField(max_length=2, choices=TYPE_CHOICES)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    description = models.TextField(blank=True)

    class Meta:
        permissions = [
            ("manage_adjustments", "Can add/change adjustments"),
        ]

    def __str__(self):
        return f"{self.get_type_display()} {self.amount} on {self.date}"

    def get_month_period(self):
        """Devolver una tupla (año, mes) para la fecha de esta transacción."""
        return (self.date.year, self.date.month)

    def save(self, *args, **kwargs):
    # Evitar modificar transacciones cuando su mes esté cerrado
        from .models import MonthPeriod  # local import
        if self.pk:
            # transacción existente: comprobar si el periodo está cerrado
            yr, m = self.get_month_period()
            try:
                mp = MonthPeriod.objects.filter(year=yr, month=m).first()
                if mp and mp.is_closed:
                    raise ValidationError('El mes está cerrado; no se pueden modificar transacciones en ese periodo.')
            except ValidationError:
                raise
            except Exception:
                # ignorar errores de consulta
                pass
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        from .models import MonthPeriod
        yr, m = self.get_month_period()
        mp = MonthPeriod.objects.filter(year=yr, month=m).first()
        if mp and mp.is_closed:
            raise ValidationError('El mes está cerrado; no se pueden eliminar transacciones en ese periodo.')
        return super().delete(*args, **kwargs)


class MonthPeriod(models.Model):
    """Representa un mes/año específico y si está cerrado."""
    year = models.PositiveIntegerField()
    month = models.PositiveIntegerField()
    is_closed = models.BooleanField(default=False)
    closed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('year', 'month')
        ordering = ['-year', '-month']
        permissions = [
            ('close_month', 'Can close month for cooperadora'),
        ]

    def __str__(self):
        return f"{self.year}-{self.month:02d}"

    def close_month(self, user=None):
        """Cerrar este MonthPeriod.

        Este método delega ahora la operación de cierre a la capa de servicios
        (MonthCloser). Mantener la orquestación en servicios facilita las pruebas
        y permite cambiar la estrategia de traslado de saldos (carryover).

        Args:
            user: usuario opcional que realiza la acción (reservado para auditoría).
        Returns:
            dict con llaves 'net' y 'carry' cuando se cierra, o None si ya estaba cerrado.
        """
        # Import service locally to avoid circular import at module load.
        from .services import MonthCloser

        closer = MonthCloser(self, user=user)
        return closer.close()

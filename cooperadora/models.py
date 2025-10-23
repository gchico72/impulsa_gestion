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
        """Return Year, Month tuple for this transaction's date."""
        return (self.date.year, self.date.month)

    def save(self, *args, **kwargs):
        # Prevent modifying transactions when their month is closed
        from .models import MonthPeriod  # local import
        if self.pk:
            # existing transaction, check if period closed
            yr, m = self.get_month_period()
            try:
                mp = MonthPeriod.objects.filter(year=yr, month=m).first()
                if mp and mp.is_closed:
                    raise ValidationError('El mes está cerrado; no se pueden modificar transacciones en ese periodo.')
            except ValidationError:
                raise
            except Exception:
                # ignore lookup errors
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
    """Represents a specific month/year and whether it's closed."""
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
        """Close this MonthPeriod.

        This method now delegates the closing operation to the service layer
        (MonthCloser). Keeping orchestration in services makes the behavior
        easier to test and allows swapping the carryover strategy.

        Args:
            user: optional user performing the action (reserved for auditing).
        Returns:
            dict with keys 'net' and 'carry' when closed, or None if already closed.
        """
        # Import service locally to avoid circular import at module load.
        from .services import MonthCloser

        closer = MonthCloser(self, user=user)
        return closer.close()

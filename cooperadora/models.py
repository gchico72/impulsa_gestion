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
        """Close the month: compute net, create carryover transaction in next month and mark closed.

        Behavior:
        - Sum incomes minus expenses and include adjustments as they are typed (AJ treated like expense or income depending on sign)
        - Create a carryover Transaction on the first day of next month with type IN or EX to reflect net
        - Mark this MonthPeriod as closed and set closed_at
        """
        if self.is_closed:
            return

        # compute net for the month
        from django.db.models import Sum
        qs = Transaction.objects.filter(date__year=self.year, date__month=self.month)
        income = qs.filter(type=Transaction.INCOME).aggregate(total=Sum('amount'))['total'] or 0
        expense = qs.filter(type=Transaction.EXPENSE).aggregate(total=Sum('amount'))['total'] or 0
        adj = qs.filter(type=Transaction.ADJUSTMENT).aggregate(total=Sum('amount'))['total'] or 0

        # define net: incomes - expenses + adjustments
        net = income - expense + adj

        # determine next month
        if self.month == 12:
            ny, nm = self.year + 1, 1
        else:
            ny, nm = self.year, self.month + 1

        # create next period record if not exists
        next_period, _ = MonthPeriod.objects.get_or_create(year=ny, month=nm)

        # create carryover transaction in next period if net != 0
        if net != 0:
            # decide type and positive amount
            if net > 0:
                ttype = Transaction.INCOME
                amt = net
            else:
                ttype = Transaction.EXPENSE
                amt = -net

            carry_date = date(ny, nm, 1)
            Transaction.objects.create(date=carry_date, type=ttype, amount=amt,
                                       description=f"Saldo trasladado desde {self.year}-{self.month:02d}")

        self.is_closed = True
        self.closed_at = timezone.now()
        self.save()

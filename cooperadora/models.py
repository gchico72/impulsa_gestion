from django.db import models


class Transaction(models.Model):
    INCOME = 'IN'
    EXPENSE = 'EX'
    TYPE_CHOICES = [
        (INCOME, 'Ingreso'),
        (EXPENSE, 'Egreso'),
    ]

    date = models.DateField()
    type = models.CharField(max_length=2, choices=TYPE_CHOICES)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.get_type_display()} {self.amount} on {self.date}"


class CooperadoraProject(models.Model):
    title = models.CharField(max_length=255)
    budget = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title

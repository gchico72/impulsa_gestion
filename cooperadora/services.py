"""Service layer for cooperadora domain logic.

This module provides:
- TransactionFactory: centralized creation of Transaction objects (factory pattern).
- CarryoverStrategy: strategy for creating carryover transactions when closing a period.
- MonthCloser: orchestrator that computes the period net and applies the carryover strategy
  (strategy pattern + service class).

Placing this logic in a separate module improves testability and keeps models thin.
"""
from datetime import date
from django.utils import timezone
from django.apps import apps
from django.db.models import Sum


class TransactionFactory:
    """Factory for creating Transaction instances.

    Use this factory so creation is centralized (single place to change behavior,
    add logging, auditing, or other side effects).
    """

    @staticmethod
    def create(date_, ttype, amount, description=None):
        Transaction = apps.get_model('cooperadora', 'Transaction')
        return Transaction.objects.create(date=date_, type=ttype, amount=amount, description=description or '')


class CarryoverStrategy:
    """Default carryover strategy.

    When a month is closed this strategy will create a carryover transaction
    on the first day of the next month. Positive net -> IN, negative net -> EX.
    """

    def create_carryover(self, year, month, net):
        """Create a carryover transaction for next month based on net amount.

        Args:
            year (int): year of closed period
            month (int): month of closed period (1-12)
            net (Decimal): net amount (income - expense + adjustments)
        Returns:
            Transaction instance or None if net == 0
        """
        if net == 0:
            return None

        # Determine next month/year
        if month == 12:
            ny, nm = year + 1, 1
        else:
            ny, nm = year, month + 1

        TransactionFactory = TransactionFactory  # local name clarity
        if net > 0:
            ttype = apps.get_model('cooperadora', 'Transaction').INCOME
            amt = net
        else:
            ttype = apps.get_model('cooperadora', 'Transaction').EXPENSE
            amt = -net

        carry_date = date(ny, nm, 1)
        return TransactionFactory.create(carry_date, ttype, amt, description=f"Saldo trasladado desde {year}-{month:02d}")


class MonthCloser:
    """Service to close a month period.

    This class encapsulates the steps of computing the net for a month, invoking
    a carryover strategy if needed and marking the MonthPeriod as closed.
    It uses apps.get_model to avoid circular imports from models -> services -> models.
    """

    def __init__(self, month_period, user=None, carryover_strategy=None):
        self.month_period = month_period
        self.user = user
        self.strategy = carryover_strategy or CarryoverStrategy()

    def compute_net(self):
        """Compute net = total incomes - total expenses + total adjustments for the period."""
        Transaction = apps.get_model('cooperadora', 'Transaction')
        qs = Transaction.objects.filter(date__year=self.month_period.year, date__month=self.month_period.month)
        income = qs.filter(type=Transaction.INCOME).aggregate(total=Sum('amount'))['total'] or 0
        expense = qs.filter(type=Transaction.EXPENSE).aggregate(total=Sum('amount'))['total'] or 0
        adj = qs.filter(type=Transaction.ADJUSTMENT).aggregate(total=Sum('amount'))['total'] or 0
        return income - expense + adj

    def close(self):
        """Perform closing: compute net, create carryover (if required) and mark closed."""
        if self.month_period.is_closed:
            return None

        net = self.compute_net()

        # Ensure next period exists (create if missing)
        MonthPeriod = apps.get_model('cooperadora', 'MonthPeriod')
        if self.month_period.month == 12:
            ny, nm = self.month_period.year + 1, 1
        else:
            ny, nm = self.month_period.year, self.month_period.month + 1

        MonthPeriod.objects.get_or_create(year=ny, month=nm)

        # Create carryover using strategy
        carry = None
        if net != 0:
            carry = self.strategy.create_carryover(self.month_period.year, self.month_period.month, net)

        # Mark closed
        self.month_period.is_closed = True
        self.month_period.closed_at = timezone.now()
        self.month_period.save()

        return {
            'net': net,
            'carry': carry,
        }

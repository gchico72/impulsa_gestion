"""Capa de servicios para la lógica de dominio de cooperadora.

Este módulo provee:
- TransactionFactory: creación centralizada de objetos Transaction (patrón factory).
- CarryoverStrategy: estrategia para crear transacciones de traslado al cerrar un periodo.
- MonthCloser: orquestador que calcula el neto del periodo y aplica la estrategia de traslado
    (patrón strategy + clase de servicio).

Colocar esta lógica en un módulo separado mejora la testeabilidad y mantiene los modelos ligeros.
"""
from datetime import date
from django.utils import timezone
from django.apps import apps
from django.db.models import Sum


class TransactionFactory:
    """Fábrica para crear instancias de Transaction.

    Usar esta fábrica centraliza la creación (un único lugar para cambiar el
    comportamiento, agregar logging, auditoría u otros efectos secundarios).
    """

    @staticmethod
    def create(date_, ttype, amount, description=None):
        Transaction = apps.get_model('cooperadora', 'Transaction')
        return Transaction.objects.create(date=date_, type=ttype, amount=amount, description=description or '')


class CarryoverStrategy:
    """Estrategia por defecto para el traslado de saldos.

    Cuando se cierra un mes, esta estrategia crea una transacción de traslado
    el primer día del mes siguiente. Neto positivo -> IN, neto negativo -> EX.
    """

    def create_carryover(self, year, month, net):
        """Crear una transacción de traslado para el mes siguiente basada en el neto.

        Args:
            year (int): año del periodo cerrado
            month (int): mes del periodo cerrado (1-12)
            net (Decimal): monto neto (ingresos - egresos + ajustes)
        Returns:
            instancia de Transaction o None si net == 0
        """
        if net == 0:
            return None

        # Determinar mes/año siguiente
        if month == 12:
            ny, nm = year + 1, 1
        else:
            ny, nm = year, month + 1

        TransactionFactory = TransactionFactory  # nombre local por claridad
        if net > 0:
            ttype = apps.get_model('cooperadora', 'Transaction').INCOME
            amt = net
        else:
            ttype = apps.get_model('cooperadora', 'Transaction').EXPENSE
            amt = -net

        carry_date = date(ny, nm, 1)
        return TransactionFactory.create(carry_date, ttype, amt, description=f"Saldo trasladado desde {year}-{month:02d}")


class MonthCloser:
    """Servicio para cerrar un periodo mensual.

    Esta clase encapsula los pasos de calcular el neto de un mes, invocar
    una estrategia de traslado si es necesario y marcar el MonthPeriod como cerrado.
    Usa apps.get_model para evitar importaciones circulares entre modelos y servicios.
    """

    def __init__(self, month_period, user=None, carryover_strategy=None):
        self.month_period = month_period
        self.user = user
        self.strategy = carryover_strategy or CarryoverStrategy()

    def compute_net(self):
        """Calcular net = total ingresos - total egresos + total ajustes para el periodo."""
        Transaction = apps.get_model('cooperadora', 'Transaction')
        qs = Transaction.objects.filter(date__year=self.month_period.year, date__month=self.month_period.month)
        income = qs.filter(type=Transaction.INCOME).aggregate(total=Sum('amount'))['total'] or 0
        expense = qs.filter(type=Transaction.EXPENSE).aggregate(total=Sum('amount'))['total'] or 0
        adj = qs.filter(type=Transaction.ADJUSTMENT).aggregate(total=Sum('amount'))['total'] or 0
        return income - expense + adj

    def close(self):
        """Realizar el cierre: calcular neto, crear traslado (si corresponde) y marcar como cerrado."""
        if self.month_period.is_closed:
            return None

        net = self.compute_net()

    # Asegurar que exista el siguiente periodo (crear si falta)
        MonthPeriod = apps.get_model('cooperadora', 'MonthPeriod')
        if self.month_period.month == 12:
            ny, nm = self.month_period.year + 1, 1
        else:
            ny, nm = self.month_period.year, self.month_period.month + 1

        MonthPeriod.objects.get_or_create(year=ny, month=nm)

    # Crear traslado usando la estrategia
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

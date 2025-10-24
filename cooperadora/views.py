from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from .models import Transaction
from .forms import TransactionForm
from . import services


def index(request):
    return render(request, 'cooperadora/index.html', {})


class TransactionListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Transaction
    template_name = 'cooperadora/transaction_list.html'
    context_object_name = 'transactions'
    permission_required = 'cooperadora.view_transaction'

    def get_context_data(self, **kwargs):
        """Agregar al contexto la separación de ingresos/egresos y los totales."""
        ctx = super().get_context_data(**kwargs)
        qs = self.get_queryset().order_by('date')
        from decimal import Decimal

        rows = []
        total_income = Decimal('0')
        total_expense = Decimal('0')
        for t in qs:
            amt = t.amount
            income_col = None
            expense_col = None
            if t.type == Transaction.INCOME:
                income_col = amt
                total_income += Decimal(amt)
            elif t.type == Transaction.EXPENSE:
                expense_col = -Decimal(amt)
                total_expense += -Decimal(amt)
            else:  # ADJUSTMENT
                if amt >= 0:
                    income_col = amt
                    total_income += Decimal(amt)
                else:
                    expense_col = Decimal(amt)
                    total_expense += Decimal(amt)

            rows.append({
                'pk': t.pk,
                'date': t.date,
                'type': t.get_type_display(),
                'income': income_col,
                'expense': expense_col,
                'description': t.description or '',
            })

        total_general = total_income + total_expense
        ctx.update({
            'rows': rows,
            'total_income': total_income,
            'total_expense': total_expense,
            'total_general': total_general,
        })
        return ctx


class TransactionCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Transaction
    form_class = TransactionForm
    template_name = 'cooperadora/transaction_form.html'
    success_url = reverse_lazy('cooperadora:transaction_list')
    permission_required = 'cooperadora.add_transaction'

    def get_initial(self):
        """Proveer datos iniciales para el formulario (fecha por defecto = hoy)."""
        initial = super().get_initial()
    # TransactionForm ya establece hoy como valor por defecto, pero lo dejamos explícito
        from datetime import date
        initial.setdefault('date', date.today())
        return initial

class TransactionUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Transaction
    form_class = TransactionForm
    template_name = 'cooperadora/transaction_form.html'
    success_url = reverse_lazy('cooperadora:transaction_list')
    permission_required = 'cooperadora.change_transaction'


class TransactionDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Transaction
    template_name = 'cooperadora/transaction_confirm_delete.html'
    success_url = reverse_lazy('cooperadora:transaction_list')
    permission_required = 'cooperadora.delete_transaction'





from django.views import View
from django.shortcuts import get_object_or_404
from django.contrib import messages


class CloseMonthView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'cooperadora.close_month'

    def get(self, request, year, month):
        # mostrar confirmación
        mp = get_object_or_404(__import__('cooperadora.models', fromlist=['MonthPeriod']).models.MonthPeriod, year=year, month=month)
        return render(request, 'cooperadora/close_month_confirm.html', {'period': mp})

    def post(self, request, year, month):
        mp = get_object_or_404(__import__('cooperadora.models', fromlist=['MonthPeriod']).models.MonthPeriod, year=year, month=month)
        try:
            # Usar la capa de servicios MonthCloser para el comportamiento de cierre
            result = services.MonthCloser(mp, user=request.user).close()
            if result is None:
                messages.info(request, f'El mes {mp} ya estaba cerrado.')
            else:
                messages.success(request, f'Mes {mp} cerrado correctamente. Neto: {result.get("net")}')
        except Exception as e:
            messages.error(request, f'Error cerrando mes: {e}')
        return redirect('cooperadora:index')


from django.http import HttpResponse
import csv
from django.utils.dateparse import parse_date
from decimal import Decimal


class TransactionReportView(LoginRequiredMixin, PermissionRequiredMixin, View):
    """Reporte de transacciones entre dos fechas (inclusivas). Soporta exportar CSV con ?format=csv."""
    permission_required = 'cooperadora.view_transaction'

    def get(self, request):
        # leer parámetros de consulta opcionales
        desde = request.GET.get('desde')
        hasta = request.GET.get('hasta')
        fmt = request.GET.get('format')

        qs = Transaction.objects.all().order_by('date')
        errors = []

        if desde:
            d = parse_date(desde)
            if not d:
                errors.append('Fecha "desde" inválida')
            else:
                qs = qs.filter(date__gte=d)
        if hasta:
            h = parse_date(hasta)
            if not h:
                errors.append('Fecha "hasta" inválida')
            else:
                qs = qs.filter(date__lte=h)

    # Construir filas con columnas separadas para ingreso/egreso
        rows = []
        total_income = Decimal('0')
        total_expense = Decimal('0')
        for t in qs:
            amt = t.amount
            income_col = None
            expense_col = None
            # Ingresos: type IN always positive
            if t.type == Transaction.INCOME:
                income_col = amt
                total_income += Decimal(amt)
            # Egresos: type EX shown as negative value in expense column
            elif t.type == Transaction.EXPENSE:
                expense_col = -Decimal(amt)
                total_expense += -Decimal(amt)
            # Ajustes: place according to sign
            else:  # ADJUSTMENT
                if amt >= 0:
                    income_col = amt
                    total_income += Decimal(amt)
                else:
                    expense_col = Decimal(amt)  # amt is negative
                    total_expense += Decimal(amt)

            rows.append({
                'date': t.date,
                'type': t.get_type_display(),
                'income': income_col,
                'expense': expense_col,
                'description': t.description or '',
            })

    # Total neto (ingresos + egresos, donde los egresos están como negativos)
        total_general = total_income + total_expense

    # Si se solicita CSV, enviarlo en streaming con columnas separadas
        if fmt == 'csv' and not errors:
            resp = HttpResponse(content_type='text/csv')
            resp['Content-Disposition'] = 'attachment; filename="cooperadora_report.csv"'
            writer = csv.writer(resp)
            writer.writerow(['date', 'type', 'income', 'expense', 'description'])
            for r in rows:
                writer.writerow([
                    r['date'].isoformat(),
                    r['type'],
                    str(r['income']) if r['income'] is not None else '',
                    str(r['expense']) if r['expense'] is not None else '',
                    r['description'],
                ])
            # Fila de totales
            writer.writerow([])
            writer.writerow(['Totales', '', str(total_income), str(total_expense), ''])
            writer.writerow(['Total general', '', str(total_general), '', ''])
            return resp

        return render(request, 'cooperadora/report.html', {
            'transactions': rows,
            'errors': errors,
            'desde': desde or '',
            'hasta': hasta or '',
            'total_income': total_income,
            'total_expense': total_expense,
            'total_general': total_general,
        })

from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from .models import Transaction


def index(request):
    return render(request, 'cooperadora/index.html', {})


class TransactionListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Transaction
    template_name = 'cooperadora/transaction_list.html'
    context_object_name = 'transactions'
    permission_required = 'cooperadora.view_transaction'


class TransactionCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Transaction
    fields = ['date', 'type', 'amount', 'description']
    template_name = 'cooperadora/transaction_form.html'
    success_url = reverse_lazy('cooperadora:transaction_list')
    permission_required = 'cooperadora.add_transaction'


class TransactionUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Transaction
    fields = ['date', 'type', 'amount', 'description']
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
        # show confirmation
        mp = get_object_or_404(__import__('cooperadora.models', fromlist=['MonthPeriod']).models.MonthPeriod, year=year, month=month)
        return render(request, 'cooperadora/close_month_confirm.html', {'period': mp})

    def post(self, request, year, month):
        mp = get_object_or_404(__import__('cooperadora.models', fromlist=['MonthPeriod']).models.MonthPeriod, year=year, month=month)
        try:
            # Use the service layer MonthCloser for closing behavior
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


class TransactionReportView(LoginRequiredMixin, PermissionRequiredMixin, View):
    """Report transactions between two dates (inclusive). Supports CSV export via ?format=csv."""
    permission_required = 'cooperadora.view_transaction'

    def get(self, request):
        # read optional query params
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

        # If CSV requested, stream it
        if fmt == 'csv' and not errors:
            resp = HttpResponse(content_type='text/csv')
            resp['Content-Disposition'] = 'attachment; filename="cooperadora_report.csv"'
            writer = csv.writer(resp)
            writer.writerow(['date', 'type', 'amount', 'description'])
            for t in qs:
                writer.writerow([t.date.isoformat(), t.get_type_display(), str(t.amount), t.description or ''])
            return resp

        return render(request, 'cooperadora/report.html', {'transactions': qs, 'errors': errors, 'desde': desde or '', 'hasta': hasta or ''})

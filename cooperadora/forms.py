from django import forms
from .models import Transaction
from datetime import date


class TransactionForm(forms.ModelForm):
    """Form for Transaction with Spanish labels and a date picker widget.

    - Sets field labels in Spanish.
    - Uses HTML5 date input for better UX in modern browsers.
    """

    class Meta:
        model = Transaction
        fields = ['date', 'type', 'amount', 'description']
        labels = {
            'date': 'Fecha',
            'type': 'Tipo',
            'amount': 'Monto',
            'description': 'Descripción',
        }
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'type': forms.Select(),
            'amount': forms.NumberInput(attrs={'step': '0.01'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        # If no initial date provided, default to today for convenience
        if 'initial' not in kwargs:
            kwargs['initial'] = {}
        kwargs['initial'].setdefault('date', date.today())
        super().__init__(*args, **kwargs)

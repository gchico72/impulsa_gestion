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
            # Render the transaction type as radio buttons (only one selectable)
            'type': forms.RadioSelect(),
            'amount': forms.NumberInput(attrs={'step': '0.01'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        # If no initial date provided, default to today for convenience
        if 'initial' not in kwargs:
            kwargs['initial'] = {}
        kwargs['initial'].setdefault('date', date.today())
        super().__init__(*args, **kwargs)
        # Only present the two core transaction types to the user (Ingreso/Egreso).
        # The model still keeps the ADJUSTMENT choice for internal operations, but
        # the form should limit the user to IN/EX options and render them as radios.
        try:
            from .models import Transaction as T
            self.fields['type'].choices = [
                (T.INCOME, T.TYPE_CHOICES[0][1]),
                (T.EXPENSE, T.TYPE_CHOICES[1][1]),
            ]
        except Exception:
            # If anything goes wrong, fall back to whatever the model provides.
            pass

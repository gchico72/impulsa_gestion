from django import forms
from .models import Transaction
from datetime import date


class TransactionForm(forms.ModelForm):
    """Formulario para Transaction con etiquetas en español y selector de fecha.

    - Establece las etiquetas de los campos en español.
    - Usa el input HTML5 de tipo date para mejor UX en navegadores modernos.
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
            # Renderizar el tipo de transacción como botones de opción (solo uno seleccionable)
            'type': forms.RadioSelect(),
            'amount': forms.NumberInput(attrs={'step': '0.01'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        # Si no se provee fecha inicial, usar hoy por conveniencia
        if 'initial' not in kwargs:
            kwargs['initial'] = {}
        kwargs['initial'].setdefault('date', date.today())
        super().__init__(*args, **kwargs)
        # Mostrar solo los dos tipos principales al usuario (Ingreso/Egreso).
        # El modelo mantiene la opción AJ para usos internos, pero el formulario
        # debe limitar al usuario a IN/EX y presentarlos como radios.
        try:
            from .models import Transaction as T
            self.fields['type'].choices = [
                (T.INCOME, T.TYPE_CHOICES[0][1]),
                (T.EXPENSE, T.TYPE_CHOICES[1][1]),
            ]
        except Exception:
            # Si algo falla, volver al comportamiento por defecto del modelo.
            pass

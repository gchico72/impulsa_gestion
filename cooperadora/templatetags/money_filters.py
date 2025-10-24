from django import template

register = template.Library()


@register.filter()
def money(value, currency='ARS'):
    """Formatea un valor numérico como una cadena monetaria usando separadores al estilo local.

    Args:
        value: valor numérico a formatear
        currency: código de moneda (por defecto 'ARS'). Soportadas: 'ARS', 'USD'.

    Comportamiento:
    - Mapea el código de moneda a un símbolo (ARS -> '$', USD -> 'US$').
    - Separador de miles es '.' y separador decimal es ',' (estilo es-AR).
    - Siempre muestra dos decimales.

    Ejemplo: 1234.5 -> "ARS -> $ 1.234,50"
    Valores negativos preservan el signo menos: -200 -> "- $ 200,00"
    """
    try:
        # Convertir a float/Decimal-compatible
        val = float(value)
    except Exception:
        return value

    # Mapear código de moneda a símbolo
    symbols = {
        'ARS': '$',
        'USD': 'US$'
    }
    symbol = symbols.get(str(currency).upper(), str(currency))

    negative = val < 0
    val = abs(val)

    # Formatear primero con separadores estilo US: 1,234.56
    s = f"{val:,.2f}"

    # Convertir a estilo es-AR: 1.234,56
    # Usar un placeholder para evitar colisiones
    s = s.replace(',', 'X').replace('.', ',').replace('X', '.')

    # Devolver con el símbolo pegado al número (sin espacios extra),
    # y poner el signo menos antes del símbolo para valores negativos.
    if negative:
        return f"-{symbol}{s}"
    return f"{symbol}{s}"

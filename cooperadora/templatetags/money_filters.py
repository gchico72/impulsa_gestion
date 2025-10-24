from django import template

register = template.Library()


@register.filter()
def money(value, currency='ARS'):
    """Format a numeric value as a monetary string using locale-style separators.

    Args:
        value: numeric value to format
        currency: currency code (default 'ARS'). Supported: 'ARS', 'USD'.

    Behavior:
    - Maps currency code to a symbol (ARS -> '$', USD -> 'US$').
    - Thousands separator is '.' and decimal separator is ',' (es-AR style).
    - Always shows two decimals.

    Example: 1234.5 -> "ARS -> $ 1.234,50"
    Negative values preserve the minus sign: -200 -> "- $ 200,00"
    """
    try:
        # Convert to float/Decimal-compatible
        val = float(value)
    except Exception:
        return value

    # Map currency code to symbol
    symbols = {
        'ARS': '$',
        'USD': 'US$'
    }
    symbol = symbols.get(str(currency).upper(), str(currency))

    negative = val < 0
    val = abs(val)

    # Format with US-style separators first: 1,234.56
    s = f"{val:,.2f}"

    # Convert to es-AR style: 1.234,56
    # Use a placeholder to avoid collision
    s = s.replace(',', 'X').replace('.', ',').replace('X', '.')

    # Return with symbol attached to the number (no extra spaces),
    # and put the minus sign before the symbol for negative values.
    if negative:
        return f"-{symbol}{s}"
    return f"{symbol}{s}"

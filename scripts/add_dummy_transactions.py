import os
import sys
import random
from datetime import datetime, date, timedelta

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'impulsa.settings')

import django
django.setup()

from cooperadora.models import Transaction, MonthPeriod


def random_date(start_date, end_date):
    """Return a random date between start_date and end_date inclusive."""
    delta = (end_date - start_date).days
    if delta <= 0:
        return start_date
    rand_days = random.randint(0, delta)
    return start_date + timedelta(days=rand_days)


def ensure_month_period(d):
    yr, m = d.year, d.month
    mp, created = MonthPeriod.objects.get_or_create(year=yr, month=m)
    return mp


def main(n=50, min_amt=1000, max_amt=50000):
    start = date(2025, 8, 1)
    end = date.today()

    created = []
    for i in range(n):
        d = random_date(start, end)
        ensure_month_period(d)
        ttype = random.choice([Transaction.INCOME, Transaction.EXPENSE])
        amt = round(random.uniform(min_amt, max_amt), 2)
        desc = f"Carga masiva {i+1} - {'Ingreso' if ttype=='IN' else 'Egreso'}"
        tr = Transaction.objects.create(date=d, type=ttype, amount=amt, description=desc)
        created.append(tr)

    total_income = sum([t.amount for t in created if t.type == Transaction.INCOME])
    total_expense = sum([t.amount for t in created if t.type == Transaction.EXPENSE])

    print(f"Created {len(created)} transactions (from {start} to {end}).")
    print(f"Income count: {len([t for t in created if t.type=='IN'])}, Expense count: {len([t for t in created if t.type=='EX'])}")
    print(f"Total income: {total_income}")
    print(f"Total expense: {total_expense}")


if __name__ == '__main__':
    main()

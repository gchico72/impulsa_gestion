"""Seed initial data for the `courses` app.

Creates Levels (Primero/Segundo/Tercero), Divisions (A/B/C),
an example Specialty and one Course for quick verification in admin.
"""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'impulsa.settings')

import django
django.setup()

from courses.models import Level, Division, Specialty, Course


def seed():
    levels = [
        ('Primero', 1),
        ('Segundo', 2),
        ('Tercero', 3),
    ]
    for name, order in levels:
        Level.objects.get_or_create(name=name, order=order)

    for d in ['A', 'B', 'C']:
        Division.objects.get_or_create(name=d)

    spec, _ = Specialty.objects.get_or_create(name='Ciencias Naturales', code='CN')

    # Create sample course Primero A - Ciencias Naturales
    lvl = Level.objects.get(order=1)
    div = Division.objects.get(name='A')
    Course.objects.get_or_create(level=lvl, division=div, specialty=spec)

    print('Seed complete: Levels, Divisions, Specialty and sample Course created.')


if __name__ == '__main__':
    seed()

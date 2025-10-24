import os
import sys
import traceback

# Ensure project root is on sys.path
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'impulsa.settings')

try:
    import django
    django.setup()
    import importlib
    importlib.import_module('cooperadora.templatetags.money_filters')
    print('IMPORT_OK')
except Exception:
    traceback.print_exc()
    sys.exit(2)

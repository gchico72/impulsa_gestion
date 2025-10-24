import os, sys, traceback
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
os.environ.setdefault('DJANGO_SETTINGS_MODULE','impulsa.settings')

try:
    import django
    django.setup()
    from django.template import loader
    t = loader.get_template('cooperadora/transaction_list.html')
    print('Template cargada OK, ahora renderizo...')
    print(t.render({}))
except Exception:
    traceback.print_exc()
    sys.exit(2)

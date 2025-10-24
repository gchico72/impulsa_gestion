import os
import sys
import traceback

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'impulsa.settings')

import django
from django.test import Client

def do_request(path, client):
    try:
        r = client.get(path, HTTP_HOST='127.0.0.1')
        print(f"{path} -> status {r.status_code}")
        body = r.content.decode('utf-8', 'ignore')
        print(body[:2000])
    except Exception:
        traceback.print_exc()


if __name__ == '__main__':
    django.setup()
    from django.contrib.auth import get_user_model
    User = get_user_model()
    # Crear u obtener un usuario de prueba
    user, created = User.objects.get_or_create(username='testuser', defaults={'email': 'test@local'})
    if created:
        user.set_password('password')
        user.is_staff = True
        user.save()

    client = Client()
    # Usar force_login para evitar lidiar con hashing de contraseñas
    client.force_login(user)

    do_request('/cooperadora/transactions/', client)
    print('\n---\n')
    do_request('/cooperadora/report/', client)
    print('\n---\n')
    do_request('/cooperadora/transactions/add/', client)
    # Verificación rápida: comprobar si la respuesta contiene inputs radio para 'type'
    r = client.get('/cooperadora/transactions/add/', HTTP_HOST='127.0.0.1')
    body = r.content.decode('utf-8', 'ignore')
    print('\nRadio inputs present? ->', 'type="radio"' in body)
    # Print a short snippet around the first radio input if present
    idx = body.find('type="radio"')
    if idx != -1:
        start = max(0, idx-120)
        end = min(len(body), idx+120)
        print(body[start:end])

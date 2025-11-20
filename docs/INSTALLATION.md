# Instalación y puesta en marcha — Impulsa Gestión

Este documento describe los pasos para instalar y ejecutar localmente el proyecto `impulsa_gestion`.
Incluye instrucciones para Windows (PowerShell) y notas para entornos Unix.

## Requisitos previos
- Python 3.10+ (recomendado 3.11/3.12)
- Git
- Opcional: `virtualenv` o usar `python -m venv`

## Clonar el repositorio
```powershell
# Desde PowerShell
cd C:\ruta\donde\quieres\proyectos
git clone <REPO_REMOTE_URL> impulsa_gestion
cd impulsa_gestion
```

Reemplaza `<REPO_REMOTE_URL>` por la URL de tu repositorio (GitHub/GitLab).

## Crear y activar entorno virtual (Windows PowerShell)
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
# Si la política de ejecución bloquea el script, ejecuta (como administrador):
# Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

En Linux/macOS:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

## Instalar dependencias
```powershell
pip install --upgrade pip
pip install -r requirements.txt
```

Nota: `requirements.txt` contiene las dependencias registradas del proyecto.

## Variables de entorno y configuración básica
Para desarrollo no es obligatorio, pero podés definir algunas variables:
- `DJANGO_SECRET` — clave secreta (si no se define usa una por defecto en `settings.py` para dev).

En PowerShell (temporal para la sesión):
```powershell
$env:DJANGO_SECRET = 'mi-clave-secreta-para-dev'
```

En Linux/macOS (temporales):
```bash
export DJANGO_SECRET='mi-clave-secreta-para-dev'
```

Para producción, guardá secretos en un archivo `.env` o en el sistema de variables seguro.

## Migraciones y base de datos
El proyecto usa SQLite por defecto (`db.sqlite3`).

Crear y aplicar migraciones:
```powershell
py manage.py makemigrations
py manage.py migrate
```

Si necesitás crear migraciones para apps concretas:
```powershell
py manage.py makemigrations subjects students teachers
py manage.py migrate
```

## Crear superusuario (opcional)
```powershell
py manage.py createsuperuser
```
Sigue las instrucciones interactivas para username/email/password.

## Usuario de desarrollo (opcional)
El proyecto puede incluir un usuario de prueba que facilitamos durante desarrollo. Para crear un usuario `dev_tester` con un password simple (útil para pruebas locales), ejecutá:

```powershell
py -3 manage.py shell -c "from django.contrib.auth.models import User, Group, Permission; from django.contrib.contenttypes.models import ContentType; import django; django.setup();
username='dev_tester'; password='DevTester!2025'; u, created = User.objects.get_or_create(username=username); u.set_password(password); u.is_staff=True; u.save();
# Opcional: crear grupo y asignar permisos (subjects, students, teachers)
from django.contrib.auth.models import Group
g, _ = Group.objects.get_or_create(name='academia_admin')
for app, model in [('subjects','subject'), ('students','student'), ('teachers','teacher')]:
    for codename in ['add_'+model, 'change_'+model, 'delete_'+model, 'view_'+model]:
        try:
            p = Permission.objects.get(codename=codename)
            g.permissions.add(p)
        except Permission.DoesNotExist:
            pass
u.groups.add(g)
print('created', created)
"
```

Después podés iniciar sesión en `/login/` con `dev_tester / DevTester!2025`.

> Nota: este usuario es solo para desarrollo local. No uses credenciales débiles en producción.

## Archivos estáticos
En modo desarrollo Django sirve archivos estáticos automáticamente. Para preparar estáticos (producción o pruebas locales):
```powershell
py manage.py collectstatic
```

## Ejecutar servidor de desarrollo
```powershell
py manage.py runserver
```
Abrí en el navegador: `http://127.0.0.1:8000/`

## Pruebas y comprobaciones
- Ejecutar checks de Django:
```powershell
py manage.py check
```
- Ejecutar tests (si existen):
```powershell
py manage.py test
```

## Tareas comunes y troubleshooting
- Si aparece `no such table: ...` => ejecutá `py manage.py migrate`.
- Si Django no carga cambios de templates o CSS, refrescar navegador y vaciar cache (o usar cache-buster en `base.html`).
- Si PowerShell no permite activar el venv: ejecutar como administrador y ajustar `Set-ExecutionPolicy`.

## Notas para producción (resumen)
- Cambiar `DEBUG=False` en `impulsa/settings.py`.
- Configurar `ALLOWED_HOSTS` correctamente.
- Usar una base de datos robusta (Postgres/MySQL) para producción.
- Configurar servidor WSGI (Gunicorn/uvicorn + nginx) y SSL.
- Almacenar `DJANGO_SECRET` y credenciales en variables de entorno o un servicio de secretos.

## Estructura relevante del proyecto
- `manage.py` — script de utilidades Django
- `impulsa/` — configuración del proyecto (`settings.py`, `urls.py`)
- `core/` — modelos y utilidades compartidas
- `students/`, `teachers/`, `subjects/`, `cooperadora/`, `projects/`, `courses/` — apps principales
- `templates/` — plantillas globales y por app
- `static/` — archivos estáticos (CSS/JS)

## ¿Querés que genere también:
- Un `docs/DEVELOPMENT.md` con flujos comunes de desarrollo (tests, estilo, pre-commit)?
- Un `docker-compose.yml` básico para ejecutar el proyecto en contenedores (Postgres + Django)?

Si querés, lo creo junto con instrucciones para usarlo.

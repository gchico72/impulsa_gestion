# impulsa_gestion

Proyecto Django base para la gestión de una institución educativa.

Apps incluidas:
- core: configuración y modelos compartidos
- students: gestión de alumnos y asistencia
- courses: gestión de cursos
- teachers: gestión de docentes y asistencia
- projects: proyectos multidisciplinarios
- cooperadora: gestión de la cooperadora (ingresos/egresos/proyectos)

Instrucciones rápidas:

1. Crear y activar un virtualenv

```powershell
python -m venv .venv; .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2. Aplicar migraciones y arrancar

```powershell
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Desarrollado por Bytenco — https://www.bytenco.com.ar

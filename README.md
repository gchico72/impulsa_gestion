# impulsa_gestion

Proyecto Django base para la gestión de una institución educativa.

Resumen rápido
- Documentación de instalación y puesta en marcha: `docs/INSTALLATION.md`
- Apps principales: `core`, `students`, `courses`, `teachers`, `projects`, `cooperadora`, `subjects`

Tabla de contenido
- [Instalación (detallada)](docs/INSTALLATION.md)
- [Estructura del proyecto](#estructura-relevante-del-proyecto)

Apps incluidas:
- core: configuración y modelos compartidos
- students: gestión de alumnos y asistencia
- courses: gestión de cursos
- teachers: gestión de docentes y asistencia
- projects: proyectos multidisciplinarios
- cooperadora: gestión de la cooperadora (ingresos/egresos)
- subjects: gestión de asignaturas

Instrucciones rápidas (resumen)

1. Crear y activar un virtualenv (PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2. Aplicar migraciones y arrancar

```powershell
py manage.py migrate
py manage.py createsuperuser
py manage.py runserver
```

Desarrollado por Bytenco — https://www.bytenco.com.ar

Logos: copia los logos proporcionados por Bytenco a la carpeta `graphics/` del proyecto. Por ejemplo:

```powershell
# En Windows PowerShell, copia el logo desde tu carpeta de intercambio
Copy-Item "Z:\Personal intercambio\Bytenco\Bytenco.png" -Destination .\graphics\Bytenco.png
```

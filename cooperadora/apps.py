from django.apps import AppConfig


class CooperadoraConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cooperadora'
    verbose_name = 'Cooperadora'

    def ready(self):
    # Crear grupos por defecto y asignar permisos después de las migraciones
        from django.db.models.signals import post_migrate
        post_migrate.connect(create_cooperadora_groups, sender=self)
        # Asegurar que nuestros templatetags se importen al arrancar para que Django
        # registre la librería de tags. Esto evita errores "not a registered tag library"
        # en entornos donde el sistema de plantillas no detectó el módulo de templatetags
        # (por ejemplo si los archivos se agregaron mientras el servidor estaba en ejecución).
        try:
            import cooperadora.templatetags.money_filters  # noqa: F401
        except Exception:
            # No levantar excepción durante el arranque; el sistema de templates
            # intentará importar al renderizar y los scripts de prueba/debug
            # podrán mostrar errores de import si los hay.
            pass


def create_cooperadora_groups(sender, **kwargs):
    """Crear dos grupos para la app cooperadora:
    - Cooperadora Admin: control total (add/change/delete/view)
    - Cooperadora ReadOnly: solo permisos de lectura
    Se ejecuta después de `migrate` y es idempotente.
    """
    try:
        from django.contrib.auth.models import Group, Permission
        from django.contrib.contenttypes.models import ContentType
        from cooperadora import models as coop_models

    # Determinar permisos solo para Transaction (sin proyectos)
        perms = set()
        ct = ContentType.objects.get_for_model(coop_models.Transaction)
        for p in Permission.objects.filter(content_type=ct):
            perms.add(p)

    # Crear grupo Admin con todos los permisos
        admin_grp, created = Group.objects.get_or_create(name='Cooperadora Admin')
        admin_grp.permissions.set(perms)

    # Crear grupo ReadOnly con solo permisos de visualización
        view_perms = [p for p in perms if p.codename.startswith('view_')]
        ro_grp, created = Group.objects.get_or_create(name='Cooperadora ReadOnly')
        ro_grp.permissions.set(view_perms)
    except Exception:
    # Evitar lanzar excepciones durante las migraciones en entornos limitados
        pass

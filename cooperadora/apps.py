from django.apps import AppConfig


class CooperadoraConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cooperadora'
    verbose_name = 'Cooperadora'

    def ready(self):
        # Create default groups and assign permissions after migrations
        from django.db.models.signals import post_migrate
        post_migrate.connect(create_cooperadora_groups, sender=self)


def create_cooperadora_groups(sender, **kwargs):
    """Create two groups for the cooperadora app:
    - Cooperadora Admin: full control (add/change/delete/view)
    - Cooperadora ReadOnly: view-only permissions
    This runs after migrate and is idempotent.
    """
    try:
        from django.contrib.auth.models import Group, Permission
        from django.contrib.contenttypes.models import ContentType
        from cooperadora import models as coop_models

        # Determine permissions for Transaction only (no projects)
        perms = set()
        ct = ContentType.objects.get_for_model(coop_models.Transaction)
        for p in Permission.objects.filter(content_type=ct):
            perms.add(p)

        # Create Admin group with all perms
        admin_grp, created = Group.objects.get_or_create(name='Cooperadora Admin')
        admin_grp.permissions.set(perms)

        # Create ReadOnly group with only view perms
        view_perms = [p for p in perms if p.codename.startswith('view_')]
        ro_grp, created = Group.objects.get_or_create(name='Cooperadora ReadOnly')
        ro_grp.permissions.set(view_perms)
    except Exception:
        # Avoid raising during migrations in constrained environments
        pass

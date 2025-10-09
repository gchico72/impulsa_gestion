def user_context(request):
    """Contexto común para plantillas: roles del usuario y notificaciones (stub).

    Devuelve:
      - user_roles: lista de nombres de roles asignados al usuario (si existe Profile)
      - notifications: lista vacía de notificaciones (placeholder)
      - unread_notifications_count: entero
    """
    roles = []
    notifications = []
    unread_count = 0
    user_groups = []
    user_perms = set()
    user = getattr(request, 'user', None)
    if user and user.is_authenticated:
        try:
            profile = user.profile
            roles = [r.name for r in profile.roles.all()]
        except Exception:
            roles = []
        # user groups
        try:
            user_groups = [g.name for g in user.groups.all()]
        except Exception:
            user_groups = []
        # permissions as 'app_label.codename'
        try:
            user_perms = set([f"{p.content_type.app_label}.{p.codename}" for p in user.user_permissions.all()])
            # also include perms from groups
            for g in user.groups.all():
                for p in g.permissions.all():
                    user_perms.add(f"{p.content_type.app_label}.{p.codename}")
            # superusers have all perms
            if user.is_superuser:
                user_perms.add('__all__')
        except Exception:
            user_perms = set()
        # Placeholder: en el futuro leer model Notification relacionado al usuario
        notifications = []
        unread_count = 0
    return {
        'user_roles': roles,
        'user_groups': user_groups,
        'user_perms': user_perms,
        'notifications': notifications,
        'unread_notifications_count': unread_count,
    }

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
    user = getattr(request, 'user', None)
    if user and user.is_authenticated:
        try:
            profile = user.profile
            roles = [r.name for r in profile.roles.all()]
        except Exception:
            roles = []
        # Placeholder: en el futuro leer model Notification relacionado al usuario
        notifications = []
        unread_count = 0
    return {
        'user_roles': roles,
        'notifications': notifications,
        'unread_notifications_count': unread_count,
    }

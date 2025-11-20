from django.db import models


class Subject(models.Model):
    """Representa una asignatura con su carga horaria semanal.

    - name: nombre de la asignatura
    - weekly_hours_presential: carga horaria semanal de clases presenciales
    - weekly_hours_tutoring: carga horaria semanal de tutoría (opcional)
    """
    name = models.CharField('nombre', max_length=200, unique=True)
    weekly_hours_presential = models.PositiveIntegerField('módulos semanales presenciales', default=0)
    weekly_hours_tutoring = models.PositiveIntegerField('módulos semanales de tutoría', null=True, blank=True)

    class Meta:
        verbose_name = 'Asignatura'
        verbose_name_plural = 'Asignaturas'

    def __str__(self):
        return self.name

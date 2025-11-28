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
    GRADE_1 = '1'
    GRADE_2 = '2'
    GRADE_3 = '3'
    GRADE_CHOICES = [
        (GRADE_1, '1ero'),
        (GRADE_2, '2do'),
        (GRADE_3, '3ro'),
    ]
    grade = models.CharField('año', max_length=2, choices=GRADE_CHOICES, default=GRADE_1)

    class Meta:
        verbose_name = 'Asignatura'
        verbose_name_plural = 'Asignaturas'

    def __str__(self):
        return self.name

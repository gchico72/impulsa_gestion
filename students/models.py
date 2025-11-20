from django.db import models
from core.models import Person


class Student(Person):
    """Estudiante de la institución. Hereda atributos comunes de Person."""
    enrollment_date = models.DateField(null=True, blank=True)


class StudentAttendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField()
    present = models.BooleanField(default=True)
    notes = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Asistencia estudiante'
        verbose_name_plural = 'Asistencias estudiantes'

    def __str__(self):
        return f"{self.student} - {self.date} - {'P' if self.present else 'A'}"

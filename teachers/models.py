from django.db import models
from core.models import Person


class Teacher(Person):
    """Docente de la institución. Hereda atributos comunes de Person."""
    # Si en el futuro se necesitan campos específicos de Teacher,
    # pueden agregarse aquí.


class TeacherAttendance(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    date = models.DateField()
    present = models.BooleanField(default=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.teacher} - {self.date} - {'P' if self.present else 'A'}"

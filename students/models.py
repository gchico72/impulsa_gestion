from django.db import models


class Student(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    dni = models.CharField(max_length=20, blank=True)
    enrollment_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.last_name}, {self.first_name}"


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

from django.db import models


class Level(models.Model):
    """Academic level (Primero, Segundo, Tercero)."""
    name = models.CharField(max_length=50)
    order = models.PositiveSmallIntegerField(unique=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.name}"


class Division(models.Model):
    """Division within a level (A, B, C)."""
    name = models.CharField(max_length=10)

    class Meta:
        unique_together = ('name',)

    def __str__(self):
        return self.name


class Specialty(models.Model):
    """Optional specialty for a course (eg. Ciencias Naturales)."""
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.name


class Course(models.Model):
    """A course container combining level + division + optional specialty.

    Examples: "Primero A - Ciencias Naturales".
    """
    level = models.ForeignKey('courses.Level', on_delete=models.PROTECT, related_name='courses')
    division = models.ForeignKey('courses.Division', on_delete=models.PROTECT, related_name='courses')
    specialty = models.ForeignKey('courses.Specialty', null=True, blank=True, on_delete=models.SET_NULL, related_name='courses')
    name = models.CharField(max_length=200, blank=True)
    code = models.CharField(max_length=50, blank=True)
    description = models.TextField(blank=True)

    class Meta:
        # prefer one course per level/division/specialty tuple
        unique_together = ('level', 'division', 'specialty')

    def save(self, *args, **kwargs):
        # Auto-generate a friendly name when not provided
        if not self.name:
            parts = [str(self.level), str(self.division)]
            if self.specialty:
                parts.append(str(self.specialty))
            self.name = ' '.join(parts)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Enrollment(models.Model):
    """Link Student <-> Course. Use a string FK to avoid import cycles."""
    student = models.ForeignKey('students.Student', on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrolled_on = models.DateField(null=True, blank=True)

    class Meta:
        unique_together = ('student', 'course')

    def __str__(self):
        return f"{self.student} in {self.course}"


class CourseMaterial(models.Model):
    """Assign a Subject to a Course with an associated Teacher.

    Each CourseMaterial represents a subject being taught in a course
    by a specific teacher (e.g., "Matemática in Primero A taught by Prof. Garcia").
    """
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='materials')
    subject = models.ForeignKey('subjects.Subject', on_delete=models.CASCADE, related_name='course_materials')
    teacher = models.ForeignKey('teachers.Teacher', on_delete=models.PROTECT, related_name='course_materials')

    class Meta:
        # Prevent duplicate subject assignments in the same course
        unique_together = ('course', 'subject')

    def __str__(self):
        return f"{self.subject} in {self.course} (Prof. {self.teacher.last_name})"

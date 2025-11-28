"""Domain services for the `courses` app.

Keep business logic and orchestration here (tests can import these services).
Use `apps.get_model()` to avoid circular imports when referencing models from other apps.
"""
from django.apps import apps
from django.db import IntegrityError


class EnrollmentService:
    """Helper methods to create and move enrollments.

    Methods are intentionally small and raise clear exceptions for callers
    (views/commands/tests) to handle.
    """

    @staticmethod
    def create_enrollment(student, course, enrolled_on=None):
        """Create an Enrollment linking `student` and `course`.

        Args:
            student: either a `students.Student` instance or a PK
            course: either a `courses.Course` instance or a PK
            enrolled_on: optional date

        Returns:
            Enrollment instance

        Raises:
            IntegrityError if the enrollment already exists.
        """
        Enrollment = apps.get_model('courses', 'Enrollment')
        Student = apps.get_model('students', 'Student')
        Course = apps.get_model('courses', 'Course')

        # Accept PKs or model instances
        if not hasattr(student, 'pk'):
            student = Student.objects.get(pk=student)
        if not hasattr(course, 'pk'):
            course = Course.objects.get(pk=course)

        try:
            enr = Enrollment.objects.create(student=student, course=course, enrolled_on=enrolled_on)
            return enr
        except IntegrityError as e:
            raise IntegrityError('Enrollment already exists for this student and course') from e

    @staticmethod
    def move_enrollment(student, from_course, to_course):
        """Move an enrollment from one course to another.

        Performs basic validation and preserves `enrolled_on` when possible.
        """
        Enrollment = apps.get_model('courses', 'Enrollment')
        Student = apps.get_model('students', 'Student')
        Course = apps.get_model('courses', 'Course')

        if not hasattr(student, 'pk'):
            student = Student.objects.get(pk=student)
        if not hasattr(from_course, 'pk'):
            from_course = Course.objects.get(pk=from_course)
        if not hasattr(to_course, 'pk'):
            to_course = Course.objects.get(pk=to_course)

        try:
            enr = Enrollment.objects.get(student=student, course=from_course)
        except Enrollment.DoesNotExist:
            raise Enrollment.DoesNotExist('No existing enrollment for student in from_course')

        # ensure no duplicate at destination
        if Enrollment.objects.filter(student=student, course=to_course).exists():
            raise IntegrityError('Student already enrolled in destination course')

        enr.course = to_course
        enr.save()
        return enr

    @staticmethod
    def list_enrollments_by_level(level):
        """Return Enrollment queryset for a Level instance or PK."""
        Enrollment = apps.get_model('courses', 'Enrollment')
        Level = apps.get_model('courses', 'Level')

        if not hasattr(level, 'pk'):
            level = Level.objects.get(pk=level)

        return Enrollment.objects.filter(course__level=level)


class CourseMaterialService:
    """Helper methods to manage Subject assignments in Courses with Teachers."""

    @staticmethod
    def add_material(course, subject, teacher):
        """Assign a Subject to a Course with a Teacher.

        Args:
            course: Course instance or PK
            subject: Subject instance or PK
            teacher: Teacher instance or PK

        Returns:
            CourseMaterial instance

        Raises:
            IntegrityError if the subject is already assigned to the course.
            ValueError if teacher is not valid.
        """
        CourseMaterial = apps.get_model('courses', 'CourseMaterial')
        Course = apps.get_model('courses', 'Course')
        Subject = apps.get_model('subjects', 'Subject')
        Teacher = apps.get_model('teachers', 'Teacher')

        if not hasattr(course, 'pk'):
            course = Course.objects.get(pk=course)
        if not hasattr(subject, 'pk'):
            subject = Subject.objects.get(pk=subject)
        if not hasattr(teacher, 'pk'):
            teacher = Teacher.objects.get(pk=teacher)

        try:
            cm = CourseMaterial.objects.create(course=course, subject=subject, teacher=teacher)
            return cm
        except IntegrityError as e:
            raise IntegrityError('Subject already assigned to this course') from e

    @staticmethod
    def list_materials_by_course(course):
        """Return CourseMaterial queryset for a Course instance or PK."""
        CourseMaterial = apps.get_model('courses', 'CourseMaterial')
        Course = apps.get_model('courses', 'Course')

        if not hasattr(course, 'pk'):
            course = Course.objects.get(pk=course)

        return CourseMaterial.objects.filter(course=course).select_related('subject', 'teacher')

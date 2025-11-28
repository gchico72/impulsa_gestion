from django import forms
from django.apps import apps
from .models import Course, CourseMaterial, Enrollment


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['level', 'division', 'specialty', 'name', 'code', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }


class CourseMaterialForm(forms.ModelForm):
    class Meta:
        model = CourseMaterial
        fields = ['course', 'subject', 'teacher']


class EnrollmentForm(forms.ModelForm):
    """Form to enroll a student in a course."""
    student = forms.ModelChoiceField(
        queryset=apps.get_model('students', 'Student').objects.all(),
        label='Estudiante',
        empty_label='-- Selecciona un estudiante --'
    )

    class Meta:
        model = Enrollment
        fields = ['student', 'course']
        widgets = {
            'course': forms.HiddenInput(),
        }

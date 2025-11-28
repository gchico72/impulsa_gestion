from django import forms
from .models import Course, CourseMaterial


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

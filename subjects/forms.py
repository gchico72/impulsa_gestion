from django import forms

from .models import Subject


class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['name', 'grade', 'weekly_hours_presential', 'weekly_hours_tutoring']
        labels = {
            'name': 'Nombre de la asignatura',
            'grade': 'Año / Curso',
            'weekly_hours_presential': 'Módulos semanales presenciales',
            'weekly_hours_tutoring': 'Módulos semanales de tutoría (opcional)',
        }
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Ej. Matemática'}),
            'grade': forms.Select(),
            'weekly_hours_presential': forms.NumberInput(attrs={'min': 0, 'max': 20}),
            'weekly_hours_tutoring': forms.NumberInput(attrs={'min': 0, 'max': 20}),
        }

    def clean_weekly_hours_presential(self):
        v = self.cleaned_data.get('weekly_hours_presential')
        if v is None:
            return 0
        if v > 20:
            raise forms.ValidationError('La carga presencial no puede superar 20 módulos semanales.')
        return v

    def clean_weekly_hours_tutoring(self):
        v = self.cleaned_data.get('weekly_hours_tutoring')
        if v is None:
            return v
        if v > 20:
            raise forms.ValidationError('La carga de tutoría no puede superar 20 módulos semanales.')
        return v

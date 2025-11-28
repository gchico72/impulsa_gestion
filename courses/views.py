from django.shortcuts import render
from django.apps import apps
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib import messages

from .forms import CourseForm, CourseMaterialForm


def index(request):
    Course = apps.get_model('courses', 'Course')
    Enrollment = apps.get_model('courses', 'Enrollment')
    qs = Course.objects.select_related('level', 'division', 'specialty').all().order_by('level__order', 'division__name')

    # annotate enrollment counts in Python to avoid adding DB-specific code here
    courses = []
    for c in qs:
        count = Enrollment.objects.filter(course=c).count()
        courses.append({
            'instance': c,
            'enrollments': count,
        })

    return render(request, 'courses/index.html', {
        'courses': courses,
    })


class CourseCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'courses.add_course'
    model = apps.get_model('courses', 'Course')
    form_class = CourseForm
    template_name = 'courses/course_form.html'
    success_url = reverse_lazy('courses:index')

    def form_valid(self, form):
        resp = super().form_valid(form)
        messages.success(self.request, 'Curso creado correctamente.')
        return resp


class CourseUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'courses.change_course'
    model = apps.get_model('courses', 'Course')
    form_class = CourseForm
    template_name = 'courses/course_form.html'
    success_url = reverse_lazy('courses:index')

    def form_valid(self, form):
        resp = super().form_valid(form)
        messages.success(self.request, 'Curso actualizado correctamente.')
        return resp


class CourseDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = 'courses.delete_course'
    model = apps.get_model('courses', 'Course')
    template_name = 'courses/course_confirm_delete.html'
    success_url = reverse_lazy('courses:index')

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        resp = super().delete(request, *args, **kwargs)
        messages.success(request, f'Curso "{obj}" eliminado correctamente.')
        return resp


class CourseMaterialCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'courses.add_coursematerial'
    model = apps.get_model('courses', 'CourseMaterial')
    form_class = CourseMaterialForm
    template_name = 'courses/coursematerial_form.html'
    success_url = reverse_lazy('courses:index')

    def form_valid(self, form):
        resp = super().form_valid(form)
        messages.success(self.request, f'Materia "{form.instance.subject}" asignada al curso.')
        return resp


class CourseMaterialUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'courses.change_coursematerial'
    model = apps.get_model('courses', 'CourseMaterial')
    form_class = CourseMaterialForm
    template_name = 'courses/coursematerial_form.html'
    success_url = reverse_lazy('courses:index')

    def form_valid(self, form):
        resp = super().form_valid(form)
        messages.success(self.request, f'Materia "{form.instance.subject}" actualizada correctamente.')
        return resp


class CourseMaterialDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = 'courses.delete_coursematerial'
    model = apps.get_model('courses', 'CourseMaterial')
    template_name = 'courses/coursematerial_confirm_delete.html'
    success_url = reverse_lazy('courses:index')

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        resp = super().delete(request, *args, **kwargs)
        messages.success(request, f'Materia "{obj.subject}" eliminada del curso.')
        return resp
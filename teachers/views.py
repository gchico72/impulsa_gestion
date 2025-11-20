from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from .models import Teacher


class TeacherListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    """Lista de docentes."""
    model = Teacher
    template_name = 'teachers/teacher_list.html'
    context_object_name = 'teachers'
    permission_required = 'teachers.view_teacher'


class TeacherCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """Alta de docente."""
    model = Teacher
    fields = [
        'first_name', 'last_name', 'dni',
        'street', 'street_number', 'between_streets', 'locality', 'postal_code',
        'phone_primary', 'phone_secondary',
    ]
    template_name = 'teachers/teacher_form.html'
    permission_required = 'teachers.add_teacher'
    success_url = reverse_lazy('teachers:list')


class TeacherUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """Edición de docente."""
    model = Teacher
    fields = [
        'first_name', 'last_name', 'dni',
        'street', 'street_number', 'between_streets', 'locality', 'postal_code',
        'phone_primary', 'phone_secondary',
    ]
    template_name = 'teachers/teacher_form.html'
    permission_required = 'teachers.change_teacher'
    success_url = reverse_lazy('teachers:list')


class TeacherDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """Baja de docente."""
    model = Teacher
    template_name = 'teachers/teacher_confirm_delete.html'
    permission_required = 'teachers.delete_teacher'
    success_url = reverse_lazy('teachers:list')

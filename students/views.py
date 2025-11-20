from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from .models import Student


class StudentListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Student
    template_name = 'students/student_list.html'
    context_object_name = 'students'
    permission_required = 'students.view_student'


class StudentCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Student
    fields = [
        'first_name', 'last_name', 'dni',
        'street', 'street_number', 'between_streets', 'locality', 'postal_code',
        'phone_primary', 'phone_secondary',
        'enrollment_date',
    ]
    template_name = 'students/student_form.html'
    permission_required = 'students.add_student'
    success_url = reverse_lazy('students:list')


class StudentUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Student
    fields = [
        'first_name', 'last_name', 'dni',
        'street', 'street_number', 'between_streets', 'locality', 'postal_code',
        'phone_primary', 'phone_secondary',
        'enrollment_date',
    ]
    template_name = 'students/student_form.html'
    permission_required = 'students.change_student'
    success_url = reverse_lazy('students:list')


class StudentDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Student
    template_name = 'students/student_confirm_delete.html'
    permission_required = 'students.delete_student'
    success_url = reverse_lazy('students:list')

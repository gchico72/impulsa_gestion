from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from .models import Subject
from .forms import SubjectForm


class SubjectListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Subject
    template_name = 'subjects/subject_list.html'
    context_object_name = 'subjects'
    permission_required = 'subjects.view_subject'
    paginate_by = 20

    def get_queryset(self):
        qs = super().get_queryset().order_by('name')
        q = self.request.GET.get('q')
        if q:
            qs = qs.filter(name__icontains=q)
        return qs


class SubjectCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Subject
    form_class = SubjectForm
    template_name = 'subjects/subject_form.html'
    permission_required = 'subjects.add_subject'
    success_url = reverse_lazy('subjects:list')


class SubjectUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Subject
    form_class = SubjectForm
    template_name = 'subjects/subject_form.html'
    permission_required = 'subjects.change_subject'
    success_url = reverse_lazy('subjects:list')


class SubjectDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Subject
    template_name = 'subjects/subject_confirm_delete.html'
    permission_required = 'subjects.delete_subject'
    success_url = reverse_lazy('subjects:list')

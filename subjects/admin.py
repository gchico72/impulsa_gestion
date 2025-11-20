from django.contrib import admin
from .models import Subject


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'weekly_hours_presential', 'weekly_hours_tutoring')
    search_fields = ('name',)

from django.contrib import admin
from .models import Student, StudentAttendance


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'dni', 'enrollment_date')


@admin.register(StudentAttendance)
class StudentAttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'date', 'present')
    list_filter = ('date', 'present')

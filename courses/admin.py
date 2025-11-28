from django.contrib import admin

from .models import Level, Division, Specialty, Course, Enrollment


class EnrollmentInline(admin.TabularInline):
    model = Enrollment
    extra = 0


class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'level', 'division', 'specialty', 'code')
    list_filter = ('level', 'division', 'specialty')
    search_fields = ('name', 'code', 'specialty__name')
    inlines = [EnrollmentInline]


class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'enrolled_on')
    search_fields = ('student__last_name', 'student__first_name', 'student__dni')
    list_filter = ('course', 'course__level')


admin.site.register(Level)
admin.site.register(Division)
admin.site.register(Specialty)
admin.site.register(Course, CourseAdmin)
admin.site.register(Enrollment, EnrollmentAdmin)
from django.contrib import admin
from .models import Course, Enrollment


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'enrolled_on')

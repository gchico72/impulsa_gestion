from django.contrib import admin

from .models import Level, Division, Specialty, Course, Enrollment, CourseMaterial


class EnrollmentInline(admin.TabularInline):
    model = Enrollment
    extra = 0


class CourseMaterialInline(admin.TabularInline):
    model = CourseMaterial
    extra = 0
    raw_id_fields = ('subject', 'teacher')


class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'level', 'division', 'specialty', 'code')
    list_filter = ('level', 'division', 'specialty')
    search_fields = ('name', 'code', 'specialty__name')
    inlines = [EnrollmentInline, CourseMaterialInline]


class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'enrolled_on')
    search_fields = ('student__last_name', 'student__first_name', 'student__dni')
    list_filter = ('course', 'course__level')


admin.site.register(Level)
admin.site.register(Division)
admin.site.register(Specialty)
admin.site.register(Course, CourseAdmin)
admin.site.register(Enrollment, EnrollmentAdmin)
admin.site.register(CourseMaterial)


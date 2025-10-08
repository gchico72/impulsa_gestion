from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('students/', include('students.urls')),
    path('courses/', include('courses.urls')),
    path('teachers/', include('teachers.urls')),
    path('projects/', include('projects.urls')),
    path('cooperadora/', include('cooperadora.urls')),
]

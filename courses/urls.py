from django.urls import path
from . import views

app_name = 'courses'

urlpatterns = [
    path('', views.index, name='index'),
    path('add/', views.CourseCreateView.as_view(), name='add'),
    path('<int:pk>/edit/', views.CourseUpdateView.as_view(), name='edit'),
    path('<int:pk>/delete/', views.CourseDeleteView.as_view(), name='delete'),
    path('material/add/', views.CourseMaterialCreateView.as_view(), name='add_material'),
    path('material/<int:pk>/edit/', views.CourseMaterialUpdateView.as_view(), name='edit_material'),
    path('material/<int:pk>/delete/', views.CourseMaterialDeleteView.as_view(), name='delete_material'),
    path('enrollment/add/', views.EnrollmentCreateView.as_view(), name='add_enrollment'),
    path('enrollment/<int:pk>/delete/', views.EnrollmentDeleteView.as_view(), name='delete_enrollment'),
]

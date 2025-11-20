from django.urls import path
from . import views

app_name = 'teachers'

urlpatterns = [
    path('', views.TeacherListView.as_view(), name='list'),
    path('new/', views.TeacherCreateView.as_view(), name='create'),
    path('<int:pk>/edit/', views.TeacherUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', views.TeacherDeleteView.as_view(), name='delete'),
]

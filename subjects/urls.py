from django.urls import path
from . import views

app_name = 'subjects'

urlpatterns = [
    path('', views.SubjectListView.as_view(), name='list'),
    path('new/', views.SubjectCreateView.as_view(), name='create'),
    path('<int:pk>/edit/', views.SubjectUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', views.SubjectDeleteView.as_view(), name='delete'),
]

from django.urls import path
from . import views

app_name = 'cooperadora'

urlpatterns = [
    path('', views.index, name='index'),
    # Transactions
    path('transactions/', views.TransactionListView.as_view(), name='transaction_list'),
    path('transactions/add/', views.TransactionCreateView.as_view(), name='transaction_add'),
    path('transactions/<int:pk>/edit/', views.TransactionUpdateView.as_view(), name='transaction_edit'),
    path('transactions/<int:pk>/delete/', views.TransactionDeleteView.as_view(), name='transaction_delete'),
    # Projects
    # Projects removed — cooperadora manages only transactions/adjustments and period closing
    # Month close
    path('close/<int:year>/<int:month>/', views.CloseMonthView.as_view(), name='close_month'),
    # Reports
    path('report/', views.TransactionReportView.as_view(), name='transaction_report'),
]

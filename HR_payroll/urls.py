from django.urls import path

from .views import PayrollEmployeeListView, monthlySalary, payableAmount

app_name = 'HR_payroll'

urlpatterns = [
    path('employees/', PayrollEmployeeListView.as_view(), name='employee-list'),
    path('<int:pk>/salary/', monthlySalary, name='salary'),
    path('<int:pk>/amount/', payableAmount, name='pay-amount'),
]
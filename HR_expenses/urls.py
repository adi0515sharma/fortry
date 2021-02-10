from .views import Apply_Expenses, list_expenses_admin, my_Expence_list, detail_expense, employee_expence_total
from django.urls import path
from django.views.generic import TemplateView

app_name = 'HR_expenses'

urlpatterns = [
    path('apply/', Apply_Expenses, name='Apply_expenses'),
    path('adminlist/', list_expenses_admin, name='list_expenses'),
    path('myexpencelist/', my_Expence_list, name='my_expence_list'),
    path('detail/<int:pk>/', detail_expense, name='admin_detail'),
    path('total/', employee_expence_total, name='emp_total'),
]

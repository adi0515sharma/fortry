from django.urls import path

from .views import profile, team, EmployeeListView, EmployeeCreateView

app_name = 'HR_user_profiles'

urlpatterns = [
    path('profile/', profile, name='profile'),
    path('team/', team, name='team'),
    path('<str:user>/team/', team, name='team'),
    path('employees/', EmployeeListView.as_view(), name='employees'),
    path('create_account/', EmployeeCreateView.as_view(), name='create-account'),
]
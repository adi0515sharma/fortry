from django.urls import path, include
from . import views

app_name = 'HR_problems'

urlpatterns = [
    path('create_soft/', views.Create_Soft, name='soft_create'),
    path('view_soft/<str:pk>/', views.SProblem_view, name='view_prob'),
    path('update_soft/<str:pk>/', views.update_soft, name='update_prob'),
    path('delete_soft/<str:pk>/', views.delete_soft, name='delete_prob'),
    path('softwareProb/', views.Soft_prob_list, name='list_prob'),
    path('problems/', views.Problem, name='problems'),
    path('my_problems/', views.my_problems, name='my_problems'),
]
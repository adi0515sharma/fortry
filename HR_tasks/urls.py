from django.urls import path, include
from . import views
from .views import search

app_name = 'HR_tasks'

urlpatterns = [
    # path('home/', views.home, name='home'),
    path('HR/event/new/', views.event, name='event_new'),
	path('HR/event/edit/<int:event_id>/', views.event, name='event_edit'),
    path('HR/search/', views.search, name='search'),
    path('HR/event/edit/<int:event_id>/delete/', views.delete_event, name='delete_tab'),
    path('', views.dashboard, name='dashboard'),
    path('HR/dashboard/create/', views.create_event, name='create_event'),
    path('HR/dashboard/<str:pk>/update/', views.event_update, name='update_event'),
    path('HR/user/events/<str:pk>/', views.user_event_view, name='event_view'),
    path('HR/user/events/',views.my_event, name='my_event'),
    path('HR/admin/links/', views.Admin, name='admin'),
    path('HR/months/json/<str:pk>/', views.data, name='json_data'),
    path('HR/notification_id/<int:id>/', views.notification_id, name='notification_id'),
]
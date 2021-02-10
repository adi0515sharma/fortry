from django.urls import path
from .views import working_days, create_leave, leave_list, my_leave_list, all_approval_list, ProfileCreatePopup


app_name='HR_leaves'


urlpatterns = [
    path('working_days/', working_days, name='working-days'),
    path('apply/', create_leave, name='create-leave'),
    path('list/', leave_list, name='list_approval'),
    path('my_leave/', my_leave_list, name='my_leave_list'),
    path('AllApprovals/', all_approval_list, name='all_approvals'),
    path('profile/create/', ProfileCreatePopup, name='ProfileCreate'),
]
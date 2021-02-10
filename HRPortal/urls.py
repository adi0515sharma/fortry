from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.conf.urls.static import static
from allauth.account import views as allauth_views
from django.views.generic import TemplateView
import notifications.urls


urlpatterns = [
    path('HR/admin/', admin.site.urls),
    path(
        'accounts/password/change/',
        login_required(
            allauth_views.PasswordChangeView.as_view(success_url='/')
        ), 
        name='account_change_password'
    ),
    path('accounts/', include('allauth.urls')),
    path('', include('HR_tasks.urls', namespace='HR_tasks')),
    path('HR/inventory/', include('HR_inventory.urls', namespace='HR_inventory')),
    path('HR/user_profiles/', include('HR_user_profiles.urls' ,namespace='HR_user_profiles')),
    path('HR/leaves/', include('HR_leaves.urls' ,namespace='HR_leaves')),
    path('HR/problems/', include('HR_problems.urls', namespace='HR_problems')),
    path('HR/payroll/', include('HR_payroll.urls', namespace='HR_payroll')),
    path('inbox/notifications/', include(notifications.urls, namespace='notifications')),
    path('HR/expenses/', include('HR_expenses.urls', namespace='HR_expenses')),
    path('test/', TemplateView.as_view(template_name='base.html')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

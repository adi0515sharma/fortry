from django.shortcuts import redirect, render
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from django.utils import timezone

from .models import Salary
from .forms import MonthlySalaryForm
from HR_leaves.models import LeaveApplication, WorkingDays


class PayrollEmployeeListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'HR_user_profiles.can_evaluate_all'
    model = User
    template_name = 'HR_payroll/employee_list.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.GET.get('q')
        if search is not None:
            queryset = User.objects.filter(username__icontains=search)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['notification'] = self.request.user.notifications.unread()
        context['read_notification'] = self.request.user.notifications.read()
        return context


@login_required
@permission_required('HR_user_profiles.can_evaluate_all', raise_exception=True)
def monthlySalary(request, pk):
    user = User.objects.get(pk=pk)
    if not Salary.objects.filter(employee=user).exists():
        Salary.objects.create(employee=user)
    if request.method == 'POST':
        form = MonthlySalaryForm(request.POST, instance=user.salary)
        if form.is_valid():
            form.save()
            return redirect('HR_payroll:employee-list')
    else:
        form = MonthlySalaryForm(instance=user.salary)
    notification = request.user.notifications.unread()
    read_notification = request.user.notifications.read()
    return render(request, 'HR_payroll/salary.html', {'form': form, 'user': user, 'notification':notification, 'read_notification':read_notification})


@login_required
@permission_required('HR_user_profiles.can_evaluate_all', raise_exception=True)
def payableAmount(request, pk):
    user = User.objects.get(pk=pk)
    months = {
        1: 'january',
        2: 'february',
        3: 'march',
        4: 'april',
        5: 'may',
        6: 'june',
        7: 'july',
        8: 'august',
        9: 'september',
        10: 'october',
        11: 'november',
        12: 'december'
    }
    if not Salary.objects.filter(employee=user).exists():
        Salary.objects.create(employee=user)
    if not user.salary.amount:
        pay = '-'
        days = 0
        daily_salary = 0
    else:
        current_month = timezone.now().month
        leaves = LeaveApplication.objects.filter(employee=user).filter(start__month=current_month).filter(approved=True)
        days = 0
        for leave in leaves:
            days += (leave.end - leave.start).days + 1
        if WorkingDays.objects.count() == 0:
            WorkingDays.objects.create()
        working_days = getattr(WorkingDays.objects.first(), months[current_month])
        if not working_days:
            working_days = 24
        daily_salary = round(user.salary.amount / working_days, 2)
        pay = round(user.salary.amount - (days * daily_salary), 2)
    notification = request.user.notifications.unread()
    read_notification = request.user.notifications.read()
    context = {
        'salary': user.salary.amount,
        'amount': pay,
        'days': days,
        'daily_salary': daily_salary,
        'user': user,
        'notification':notification,
        'read_notification':read_notification
    }
    return render(request, 'HR_payroll/payable_amount.html', context)

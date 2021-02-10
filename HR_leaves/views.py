from django.shortcuts import render, redirect, reverse
from django.views.generic import CreateView
from django import forms
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User, Group
from django.http import HttpResponse, HttpResponseRedirect

from .models import WorkingDays, LeaveApplication
from .forms import CreateLeaveForm, AssignForm, ProfileForm
from notifications.signals import notify
from django.forms import modelformset_factory
from  HR_user_profiles.models import Profile
from HR_expenses.models import Expenses


@login_required
@permission_required('HR_user_profiles.can_evaluate_all', raise_exception=True)
def working_days(request):
    if WorkingDays.objects.count() == 0:
        WorkingDays.objects.create()
    days = WorkingDays.objects.all()
    day = days.first()
    notification =   request.user.notifications.unread()
    read_notification   =   request.user.notifications.read()
    values = {
        'january': day.january,
        'february': day.february,
        'march': day.march,
        'april': day.april,
        'may': day.may,
        'june': day.june,
        'july': day.july,
        'august': day.august,
        'september': day.september,
        'october': day.october,
        'november': day.november,
        'december': day.december
    }
    for month in values.keys():
        if request.GET.get(month) != '' and request.GET.get(month) is not None:
            values[month] = int(request.GET.get(month))
    days.update(
        january=values['january'],
        february=values['february'],
        march=values['march'],
        april=values['april'],
        may=values['may'],
        june=values['june'],
        july=values['july'],
        august=values['august'],
        september=values['september'],
        october=values['october'],
        november=values['november'],
        december=values['december']
        )
    values['notification'] = notification
    values['read_notification'] = read_notification
    return render(request, 'HR_leaves/working_days.html', values)



def is_valid_queryparam(param):
    return param != '' and param is not None


@login_required
@permission_required('HR_user_profiles.can_evaluate_all', raise_exception=True)
def leave_list(request):
    leaves = LeaveApplication.objects.all().filter(approved=None)
    users = User.objects.all()
    profile = Profile.objects.all()
    notification =   request.user.notifications.unread()
    read_notification   =   request.user.notifications.read()

    if request.method=='GET' and request.GET.get('ordering_by')=='date_created' and request.GET.get('asddes')=='ascending':
        leaves = leaves.order_by('-created_on')
    if request.method=='GET' and request.GET.get('asddes')=='date_created' and request.GET.get('asddes')=='descending':
        leaves = leaves.order_by('created_on')
    if request.method=='GET' and request.GET.get('ordering_by')=='date_start' and request.GET.get('asddes')=='descending':
        leaves = leaves.order_by('-start')
    if request.method=='GET' and request.GET.get('asddes')=='date_start' and request.GET.get('asddes')=='ascending':
        leaves = leaves.order_by('start')

    if request.method=='GET' and 'filter' in request.GET:
        leave_title = request.GET.get('leave_title')
        employee_name = request.GET.get('employee_name')
        assign_to = request.GET.get('assign_to')
        leave_after = request.GET.get('leave_after')
        leave_before = request.GET.get('leave_before')
        created_after = request.GET.get('created_after')
        created_before = request.GET.get('created_before')

        if is_valid_queryparam(leave_title):
            leaves = leaves.filter(title__icontains = leave_title)

        if is_valid_queryparam(employee_name):
            leaves = leaves.filter(employee__username = employee_name)

        if is_valid_queryparam(assign_to):
            leaves = leaves.filter(assign__user__username = assign_to)

        if is_valid_queryparam(leave_after):
            leaves = leaves.filter(start__gte = leave_after)

        if is_valid_queryparam(leave_before):
            leaves = leaves.filter(end__lte = leave_before)

        if is_valid_queryparam(created_after):
            leaves = leaves.filter(created_on__gte = created_after)

        if is_valid_queryparam(created_before):
            leaves = leaves.filter(created_on__lte = created_before)

    
    
    for leave in leaves:
        if request.method=='GET' and 'approve%s'%(leave.id) in request.GET:
            assign_to = request.GET.get('assign_to')
            application = LeaveApplication.objects.get(id=leave.id)
            if is_valid_queryparam(assign_to):
                application.assign__profile = assign_to
            application.approved = True
            notify.send(request.user, recipient=User.objects.get(username=application.employee), verb='Leave Application Approved' )
            application.save()
            return redirect('HR_leaves:list_approval')

    for leave in leaves:
        if request.method=='GET' and 'disapprove%s'%(leave.id) in request.GET:
            application = LeaveApplication.objects.get(id=leave.id)
            application.approved = False
            application.save()
            notify.send(request.user, recipient=User.objects.get(username=application.employee), verb='Leave Application Disapproved', target='Disapproved', description='Disapproved')
            return redirect('HR_leaves:list_approval')
   

    context = {'myList':leaves, 'users':users, 'profile':profile, 'notification':notification, 'read_notification':read_notification }
    return render(request, 'HR_leaves/list_approval.html', context)


@login_required
def create_leave(request):
    notification =   request.user.notifications.unread()
    read_notification   =   request.user.notifications.read()
    if request.method == 'POST':
        form = CreateLeaveForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.employee = request.user
            instance.save()
            notify.send(request.user, recipient=Group.objects.get(name='HR'), verb='Leave Application', description='New Application')
            return redirect('HR_tasks:dashboard')
    else:
        form = CreateLeaveForm()
        form.fields['start'].widget = forms.TextInput(attrs={'type': 'date'})
        form.fields['end'].widget = forms.TextInput(attrs={'type': 'date'})
    return render(request, 'HR_leaves/leave_form.html', {'form': form, 'notification':notification, 'read_notification':read_notification})


def my_leave_list(request):
    leaves = LeaveApplication.objects.all().filter(employee = request.user).order_by('start')
    notification =   request.user.notifications.unread()
    read_notification   =   request.user.notifications.read()
    context = { 'leaves' : leaves, 'notification':notification, 'read_notification':read_notification }
    return render(request, 'HR_leaves/my_leave_list.html', context)


@login_required
@permission_required('HR_user_profiles.can_evaluate_all', raise_exception=True)
def all_approval_list(request):
    leaves              =       LeaveApplication.objects.all().filter(approved=None)
    users               =       User.objects.all()
    expence             =       Expenses.objects.all().filter(approved=None)
    profile             =       Profile.objects.all()
    notification        =       request.user.notifications.unread()
    read_notification   =       request.user.notifications.read()


    if request.method=='GET' and request.GET.get('ordering_by')=='date_created' and request.GET.get('asddes')=='ascending':
        leaves = leaves.order_by('-created_on')
    if request.method=='GET' and request.GET.get('asddes')=='date_created' and request.GET.get('asddes')=='descending':
        leaves = leaves.order_by('created_on')
    if request.method=='GET' and request.GET.get('ordering_by')=='date_start' and request.GET.get('asddes')=='descending':
        leaves = leaves.order_by('-start')
    if request.method=='GET' and request.GET.get('asddes')=='date_start' and request.GET.get('asddes')=='ascending':
        leaves = leaves.order_by('start')

    if request.method=='GET' and 'filter' in request.GET:
        type_approval           =       request.GET.get('type_approval')
        a_title                 =       request.GET.get('a_title')
        employee_name           =       request.GET.get('employee_name')
        assign_to               =       request.GET.get('assign_to')
        leave_after             =       request.GET.get('leave_after')
        leave_before            =       request.GET.get('leave_before')
        created_after           =       request.GET.get('created_after')
        created_before          =       request.GET.get('created_before')

        if is_valid_queryparam(type_approval):
            if type_approval == 'l':
                expence      =      []
                users        =      []
            if type_approval == 'E':
                leaves      =       []
                users       =       []
            if type_approval == 'T':
                expence      =        []
                leaves       =        []
            if type_approval == 'T' and type_approval=='E':
                leaves       =        []


        if is_valid_queryparam(a_title):
            leaves      = leaves.filter(title__icontains = a_title)
            users       = users.filter(username__icontains = a_title)
            expence     = expence.filter(expense_on__icontains = a_title)

        if is_valid_queryparam(employee_name):
            leaves      = leaves.filter(employee__username = employee_name)
            users       = users.filter(username = employee_name)
            expence     = expence.filter(employee__username = employee_name)

        if is_valid_queryparam(assign_to):
            leaves = leaves.filter(assign__user__username = assign_to)

        if is_valid_queryparam(leave_after):
            leaves = leaves.filter(start__gte = leave_after)

        if is_valid_queryparam(leave_before):
            leaves = leaves.filter(end__lte = leave_before)

        if is_valid_queryparam(created_after):
            leaves = leaves.filter(created_on__gte = created_after)
            users = users.filter(date_joined__gte = created_before)
            expence = expence.filter(created_on__gte = created_before)

        if is_valid_queryparam(created_before):
            leaves = leaves.filter(created_on__lte = created_before)
            users = users.filter(date_joined__lte = created_before)
            expence = expence.filter(created_on__lte = created_before)

    
    
    for leave in leaves:
        if request.method=='GET' and 'approve%s'%(leave.id) in request.GET:
            assign_to = request.GET.get('assign_to')
            application = LeaveApplication.objects.get(id=leave.id)
            if is_valid_queryparam(assign_to):
                application.assign__profile = assign_to
            application.approved = True
            notify.send(request.user, recipient=User.objects.get(username=application.employee), verb='Leave Application Approved' )
            application.save()
            return redirect('HR_leaves:list_approval')

    for leave in leaves:
        if request.method=='GET' and 'disapprove%s'%(leave.id) in request.GET:
            application = LeaveApplication.objects.get(id=leave.id)
            application.approved = False
            application.save()
            notify.send(request.user, recipient=User.objects.get(username=application.employee), verb='Leave Application Disapproved', target='Disapproved', description='Disapproved')
            return redirect('HR_leaves:list_approval')


    # Expence list
    
    
    for exp in expence:
        if request.method=='GET' and 'approve%s'%(exp.id) in request.GET:
            expenc          =       Expenses.objects.get(id = exp.id)
            expenc.approved =       True
            notify.send(request.user, recipient=User.objects.get(username=expenc.employee), verb='Expence Approved by HR' )
            expenc.save()
            return redirect('HR_expenses:list_expenses')

        if request.method=='GET' and 'disapprove%s'%(exp.id) in request.GET:
            expenc          =       Expenses.objects.get(id = exp.id)
            expenc.approved =       False
            notify.send(request.user, recipient=User.objects.get(username=expenc.employee), verb='Expence Approved by HR' )
            expenc.save()
            return redirect('HR_expenses:list_expenses')


    context = {'myList'             :   leaves, 
                'users'             :   users, 
                'profile'           :   profile, 
                'notification'      :   notification, 
                'read_notification' :   read_notification,
                'expence'           :   expence }
    return render(request, 'All_approvals/allApproval.html', context)


def ProfileCreatePopup(request):
	form = ProfileForm(request.POST or None)
	if form.is_valid():
		instance = form.save()

		## Change the value of the "#id_author". This is the element id in the form
		
		return HttpResponse('<script>opener.closePopup(window, "%s", "%s", "#id_profile");</script>' % (instance.pk, instance))
	
	return render(request, "HR_leaves/profile_form.html", {"form" : form})


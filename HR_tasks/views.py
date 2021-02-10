from datetime import datetime, timedelta, date
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views import generic
from django.urls import reverse,resolve
from django.utils.safestring import mark_safe
import calendar
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import *
from .forms import EventForm, ApprovalForm
from django import forms
from django.contrib.auth.models import User
import json
from HR_user_profiles.models import Team, Profile
from django.template.loader import render_to_string
from .filters import EventFilter
from django.db.models import Q
from itertools import chain
from HR_problems.models import Prob_software
from HR_inventory.models import Hardware,Software,Vendor
from django.contrib.auth.decorators import login_required, permission_required
from HR_leaves.models import WorkingDays, LeaveApplication
from notifications.signals import notify
from notifications.models import Notification
from HR_payroll.models import Salary
from HR_expenses.models import Expenses
import requests




@login_required
def search(request):
    notification =   request.user.notifications.unread()
    read_notification = request.user.notifications.read()
    try:
        query = request.GET.get('q')
    except:
        query = None
    if query:
        event = Event.objects.filter(Q(title__contains=query))
        prob = Prob_software.objects.filter(Q(title__contains=query) | Q(issue__contains=query))
        hardware = Hardware.objects.filter(Q(name__icontains=query) | Q(item_type__contains=query) | Q(description__contains=query))
        software = Software.objects.filter(Q(name__icontains=query) | Q(item_type__contains=query) | Q(description__contains=query))
        vendor = Vendor.objects.filter(Q(name__icontains=query) | Q(email__contains=query) | Q(address__contains=query))
        results = list(chain(event, prob, hardware, software, vendor))
        qs = sorted(results, 
                        key=lambda instance: instance.pk, 
                        reverse=True)
        count = len(qs)
        context = { 'results':results,
                    'query':query,
                    'count':count,
                    'notification':notification,
                    'read_notification':read_notification
                    }
        template = 'tasks/result.html'
    else:
        context = {'notification': notification,
                    'read_notification':read_notification
                    }
        template = 'dashboard.html'
    
    return render(request, template, context)



@login_required
@permission_required('HR_user_profiles.can_evaluate_all', raise_exception=True)
def Admin(request):
    notification =   request.user.notifications.unread()
    read_notification = request.user.notifications.read()
    context = {
        'notification': notification,
        'read_notification':read_notification
    }
    return render(request, 'admin.html', context)




@login_required
def event(request, event_id=None):
    instance = Event()
    if event_id:
        instance = get_object_or_404(Event, pk=event_id)
    else:
        instance = Event(user=request.user)

    form = EventForm(request.POST or None, instance=instance)
    if request.POST and form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('calendar'))
    return render(request, 'tasks/events.html', {'form': form})

@login_required
def delete_event(request, event_id):
    instance = Event.objects.get(id=event_id)
    if request.method == 'POST':
        instance.delete()
        return redirect('/')
    context = {'event': instance}
    return render(request, 'tasks/delete.html', context)

@login_required
def dashboard(request, event_id=None):
    event = []
    if request.user.is_authenticated:
        event = Event.objects.filter(user=request.user)
        event_by_date = event.filter(start_time__range=[datetime.now() - timedelta(days=2), datetime.now() + timedelta(days=2)])
    else:
        return render(request,'dashboard.html')
    event_title = []
    event_date = []
    for i in event:
        event_title.append(i.title)
        event_date.append(i.start_time.strftime("%d-%m-%Y"))
    

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

    label               =       []
    data                =       []
    data2               =       []
    if not WorkingDays.objects.all():
        WorkingDays.objects.create()
    for i in range(1,13):
        days            =       0
        working_days    =       getattr(WorkingDays.objects.first(), months[i])
        if not working_days:
            working_days =      24
        data.append(working_days)
        leaves          =       LeaveApplication.objects.filter(employee=request.user).filter(start__month=i).filter(approved=True)
        for leave in leaves:
            days        +=      (leave.end - leave.start).days + 1
        data2.append(working_days-days)
        
    current_month       =       datetime.now().month
    leave_curr_month    =       LeaveApplication.objects.filter(employee=request.user).filter(start__month=current_month).filter(approved=True)
    days_curr           =       0
    for leave_curr in leave_curr_month:
        days_curr       +=      (leave_curr.end - leave_curr.start).days + 1
    
    notification        =       request.user.notifications.unread()
    read_notification   =       request.user.notifications.read()
    active_issue_count  =       Prob_software.objects.all().filter(current_status="active").filter(user=request.user).count()

    event_count                 =       Event.objects.all().filter(user=request.user).filter(start_time__month=current_month).count()
    working_days_current        =       getattr(WorkingDays.objects.first(), months[current_month])
    if not working_days_current:
        working_days_current    =       24
    percentage_work             =       (event_count*100/working_days_current)
    percentage_work             =       "%.2f" % round(percentage_work, 2)


    days_left_curr_month        =       calendar.monthrange(datetime.now().year,datetime.now().month)[1] - datetime.now().day 

    # FOR MODAL POPUP
    today_date                  =       datetime.now().date()
    event_today                 =       Event.objects.all().filter(start_time__date = today_date)

    # for feedback
    if request.method == 'GET' and 'feed' in request.GET:
        feedtype        =       request.GET.get('feedtype')
        feeddetail      =       request.GET.get('feeddetail')
        feedback        =       Feedback(type = feedtype, description= feeddetail)
        print(feedback)
        feedback.save()

    # for all approvals modal
    leaves              =       LeaveApplication.objects.all().filter(approved=None)
    users               =       User.objects.all()
    expence             =       Expenses.objects.all().filter(approved=None)
    profile             =       Profile.objects.all()

    # for approved leaves
    dash_leaves         =       request.user.leaveapplication_set.all().filter(approved=True)
    days_leave          =       []
    for i in dash_leaves:
        app_days_leaves =       i.end   -       i.start
        days_leave.append(app_days_leaves)

    label = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'June', 'July', 'August', 'Sept', 'Oct', 'Nov', 'Dec']

    return render(request, 'dashboard.html', {'event'               :   json.dumps(event_title), 
                                              'event_date'          :   json.dumps(event_date),
                                              'leaves'              :   leaves,
                                              'users'               :   users,
                                              'expence'             :   expence,
                                              'event_by_date'       :   event_by_date, 
                                              'label'               :   label, 
                                              'data'                :   data,
                                              'profile'             :   profile,
                                              'data2'               :   data2,
                                              'days_leave'          :   days_leave,
                                              'dash_leaves'         :   dash_leaves, 
                                              'notification'        :   notification, 
                                              'read_notification'   :   read_notification, 
                                              'active_issue_count'  :   active_issue_count,
                                              'leave_curr_month'    :   days_curr,
                                              'percentage_work'     :   percentage_work,
                                              'days_left_curr_month':   days_left_curr_month,
                                              'event_today'         :   event_today})

@login_required
def  save_event_form(request, form, template_name):
    data = dict()

    if request.method == 'POST':
        if form.is_valid():
            
            form.instance.user = request.user
            form.save()
            data['form_is_valid'] = True
            event = Event.objects.filter(user=request.user)
            event_by_date = event.filter(start_time__range=[datetime.now()-timedelta(days=2),datetime.now()+timedelta(days=2)])
            data['html_book_list'] = render_to_string('create_event.html', {
                'event_by_date': event_by_date
            },request=request)
        else:
            data['form_is_valid'] = False
    context = {'form': form}
    data['html_form'] = render_to_string(template_name,
        context,
        request=request,
    )
    return JsonResponse(data)

@login_required
def create_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
    else:
        form = EventForm()
    return save_event_form(request, form, 'create_event.html')

@login_required
def event_update(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
    else:
        form = EventForm(instance=event)
    return save_event_form(request, form, 'event_update.html')

@login_required
@permission_required('HR_user_profiles.can_evaluate_all', raise_exception=True)
def user_event_view(request, pk):
    today = datetime.now()
    user = User.objects.get(id=pk)
    events = user.event_set.all().order_by('start_time').filter(start_time__year=today.year, start_time__month=today.month)
    events_title = []
    events_datetime = []
    events_description = []
    events_endtime = []
    
    comments = user.approval_set.filter(year=today.year, month=today.month)
    # if comments:
    #     weeks1 = comments.filter(week1==True)
    for i in events:
        events_title.append(i.title)
        events_datetime.append(i.start_time.strftime("%Y-%m-%dT%H:%M"))
        events_description.append(i.description)
        events_endtime.append(i.end_time.strftime("%Y-%m-%dT%H:%M"))
    
    form = ApprovalForm()

    notification =   request.user.notifications.unread()
    read_notification = request.user.notifications.read()
    
    context = { 'events'                :   json.dumps(events_title),
                'events_endtime'        :   json.dumps(events_endtime),
                'events_description'    :   json.dumps(events_description),
                'events_date'           :   json.dumps(events_datetime),
                'comments'              :   comments,
                # 'weeks1'                :   weeks1,
                'user'                  :   user,
                'form'                  :   form,
                'notification'          :   notification,
                'read_notification'     :   read_notification
                }
    return render(request, 'tasks/hr_perUser_table.html', context)

def data(request , pk):
    if request.method == 'POST':
        form = ApprovalForm(request.POST)
        if form.is_valid():
            form_instance = form.save(commit=False)
            form_instance.user = User.objects.get(id=pk) 
            form_instance.year = datetime.now().year
            print(request.POST.get('week2',False))
            if request.POST['week1'] == 'yes':
                form_instance.week1 = True
            elif request.POST['week1'] == 'no':
                form_instance.week1 = False
            if request.POST['week2'] == 'yes':
                form_instance.week2 = True
            elif request.POST['week2'] == 'no':
                form_instance.week2 = False
            if request.POST['week3'] == 'yes':
                form_instance.week3 = True
            elif request.POST['week3'] == 'no':
                form_instance.week3 = False
            if request.POST['week4'] == 'yes':
                form_instance.week4 = True
            elif request.POST['week4'] == 'no':
                form_instance.week4 = False
            form_instance.save()
            return HttpResponseRedirect(reverse('HR_tasks:event_view',kwargs={'pk': pk}))

    else:
        form = ApprovalForm()
        user = User.objects.get(id=pk)
        month = request.GET.get('month', None)
        year = request.GET.get('year', None)
        approval_json = Approval.objects.filter(user=user).filter(month=month).filter(year=year)
        if approval_json:
            data = {
                'week_1' : approval_json.filter(week1=True).exists(),
                'week_2' : approval_json.filter(week2=True).exists(),
                'week_3' : approval_json.filter(week3=True).exists(),
                'week_4' : approval_json.filter(week4=True).exists(),
                'comment': list(approval_json.values('comment')),
            }
        else:
            data={
                'week_1' : "no",
                'week_2' : "no",
                'week_3' : "no",
                'week_4' : "no",
                "comment": "no",
            }
        return JsonResponse(data)



@login_required
def my_event(request):

    today = datetime.now()
    user = User.objects.get(username=request.user.username)
    notification = request.user.notifications.unread()
    read_notification = request.user.notifications.read()
    # comments = user.approval_set.all().filter(date_created__month=today.month)
    if request.method == 'POST':
        month = request.POST['month']
        # print(month)
        comments     = user.approval_set.all().filter(date_created__month=month)
    events = user.event_set.all().order_by('start_time').filter(start_time__month=today.month, start_time__year=today.year)
    events_title = []
    events_datetime = []
    events_description = []
    events_endtime = []
    for i in events:
        events_title.append(i.title)
        events_datetime.append(i.start_time.strftime("%Y-%m-%dT%H:%M"))
        events_description.append(i.description)
        events_endtime.append(i.end_time.strftime("%Y-%m-%dT%H:%M"))
    return render(request, 'tasks/my_event.html', { 'events'                :   json.dumps(events_title),
                                                    'events_endtime'        :   json.dumps(events_endtime),
                                                    'events_description'    :   json.dumps(events_description),
                                                    'events_date'           :   json.dumps(events_datetime),
                                                    # 'comments'              :   comments, 
                                                    'notification'          :   notification, 
                                                    'read_notification'     :   read_notification})

@login_required
def notification_id(request, id):
    notification    =   Notification.objects.get(id=id)
    # id              =   notification.target.id
    if notification.verb == 'Leave Application':
        notification.unread=False
        notification.save()
        return HttpResponseRedirect(reverse('HR_leaves:list_approval'))
    if notification.description == 'Expence':
        notification.unread=False
        notification.save()
        return HttpResponseRedirect(reverse('HR_expenses:list_expenses'))
    if notification.verb == 'Leave Application Approved':
        notification.unread=False
        notification.save()
        return redirect('HR_leaves:my_leave_list')
    if notification.verb == 'Leave Application Disapproved':
        notification.unread=False
        notification.save()
        return redirect('HR_leaves:my_leave_list')
    if notification.description == 'issue':
        notification.unread=False
        notification.save()
        return HttpResponseRedirect(reverse('HR_problems:list_prob'))
    return reverse('HR_tasks:dashboard')





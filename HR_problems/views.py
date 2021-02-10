from .models import *
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.db.models import Q
from .forms import *
from notifications.signals import notify
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from HR_inventory.models import Hardware, Software
from notifications.signals import notify

@login_required
def Create_Soft(request):
    form = SoftwareForm()
    if request.method == 'POST':
        form = SoftwareForm(request.POST)
        
        if form.is_valid():
            title = form.cleaned_data['title']
            issue = form.cleaned_data['issue']
            root_cause = form.cleaned_data['root_cause']
            Symptoms = form.cleaned_data['Symptoms']
            hardware_item = form.cleaned_data['hardware_item']
            software_item = form.cleaned_data['software_item']
            obj = Prob_software(title=title, 
                                issue=issue, 
                                root_cause=root_cause, 
                                Symptoms=Symptoms, 
                                hardware_item=hardware_item, 
                                software_item=software_item, 
                                user=request.user)
           
            obj.save()
            user = User.objects.get(groups__name="HR")
            notify.send(request.user, recipient=user, verb='%s reported a problem'%(request.user), description='issue')
            return redirect('HR_problems:list_prob')
    notification        =   request.user.notifications.unread()
    read_notification   =   request.user.notifications.read()
    context = {'form':form, 'notification':notification, 'read_notification':read_notification}
    return render(request, 'problems/soft_prob.html', context)

@login_required
def SProblem_view(request, pk):

    problem = get_object_or_404(Prob_software, pk=pk)
    comments = problem.comments.all()
    new_comment = None
    notification =   request.user.notifications.unread()
    read_notification   =   request.user.notifications.read()
    if request.method == 'POST' and 'comment' in request.POST:
        comment_form = CommentForm(request.POST)
        
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.issue = problem
            new_comment.user = request.user
            new_comment.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        comment_form = CommentForm()

    form = SoftUpForm(instance=problem)
    if request.method =='POST' and 'update' in request.POST:
        form = SoftUpForm(request.POST, instance=problem)
        if form.is_valid:
            form.save()
            return redirect('HR_problems:list_prob')
    context = {'problem':problem, 'form':form, 'comment_form':comment_form, 'comments':comments, 'notification':notification, 'read_notification':read_notification }
    return render(request, 'problems/Problem_view.html', context)

@login_required
def update_soft(request, pk):
    
    problem = Prob_software.objects.get(id=pk)
    form = SoftUpForm(instance=problem)
    notification =   request.user.notifications.unread()
    read_notification   =   request.user.notifications.read()
    if request.method == 'POST':
        form = SoftUpForm(request.POST, instance=problem)
        if form.is_valid:
            form.save()
            user = User.objects.get(groups__name='Employee')
            notify.send(request.user, recipient=user, verb='%s updated problem'%(request.user), description='issue', target='issue')
            return redirect('HR_problems:list_prob')
    context = { 
                'form':form,
                'notification':notification,
                'read_notification':read_notification
                }
    return render(request, 'problems/problemUpdate.html', context)


@login_required
def delete_soft(request, pk):
    problem = Prob_software.objects.get(id=pk)
    if request.method == 'POST':
        problem.delete()
        return redirect('HR_problems:list_prob')
    notification =   request.user.notifications.unread()
    read_notification   =   request.user.notifications.read()
    return render(request, 'problems/del_soft_prob.html', {'problem':problem, 'notification':notification, 'read_notification':read_notification})


def is_valid_queryparam(param):
    return param != '' and param is not None

@login_required
def Soft_prob_list(request):
    problems = Prob_software.objects.all().filter(Q(current_status='active') | Q(current_status='onGoing'))
    hardware = Hardware.objects.all()
    software = Software.objects.all()
    users = User.objects.all()
    notification =   request.user.notifications.unread()
    read_notification   =   request.user.notifications.read()
    if request.method=='GET' and request.GET.get('ordering_by')=='due_by':
        problems = problems.order_by('due_by')
    
    if request.method=='GET' and request.GET.get('asddes')=='descending':
        problems = problems.order_by('-due_by')

    if request.method=='GET' and 'filter' in request.GET:
        issue_title = request.GET.get('issue_title')
        due_before = request.GET.get('due_before')
        priority = request.GET.get('priority')
        impact = request.GET.get('impact')
        hardware_item = request.GET.get('hardware_item')
        software_item = request.GET.get('software_item')
        user_name = request.GET.get('user_name')

        if is_valid_queryparam(issue_title):
            problems = problems.filter(title__icontains = issue_title)
        if is_valid_queryparam(due_before):
            problems = problems.filter(due_by__lte = due_before)
        if is_valid_queryparam(priority):
            problems = problems.filter(priority__icontains = priority)
        if is_valid_queryparam(impact):
            problems = problems.filter(impact__icontains = impact)
        if is_valid_queryparam(hardware_item):
            problems = problems.filter(hardware_item__name = hardware_item)
        if is_valid_queryparam(software_item):
            problems = problems.filter(software_item__name = software_item)
        if is_valid_queryparam(software_item):
            problems = problems.filter(user__username = user_name)



    context = {'problems':problems,
                'hardware':hardware, 
                'software':software, 
                'users':users,
                'notification':notification, 
                'read_notification':read_notification
                }
    return render(request, 'problems/Sprob_list.html', context)


@login_required
def Problem(request):
    notification = request.user.notifications.unread()
    read_notification   =   request.user.notifications.read()
    context = { 'notification': notification, 'read_notification':read_notification }
    return render(request, 'problems/problems.html', context)


@login_required
def my_problems(request):

    problems = Prob_software.objects.all().filter(user = request.user)
    notification = request.user.notifications.unread()
    read_notification   =   request.user.notifications.read()

    if request.method=='GET' and request.GET.get('ordering_by')=='due_by':
        problems = problems.order_by('due_by')
    
    if request.method=='GET' and request.GET.get('asddes')=='descending':
        problems = problems.order_by('-due_by')
    
    if request.method=='GET' and request.GET.get('asddes')=='ascending':
        problems = problems.order_by('due_by')

    if request.method=='GET' and 'filter' in request.GET:
        issue_title = request.GET.get('issue_title')
        due_before = request.GET.get('due_before')
        priority = request.GET.get('priority')
        impact = request.GET.get('impact')
        hardware_item = request.GET.get('hardware_item')
        software_item = request.GET.get('software_item')

        if is_valid_queryparam(issue_title):
            problems = problems.filter(title__icontains = issue_title)
        if is_valid_queryparam(due_before):
            problems = problems.filter(due_by__lte = due_before)
        if is_valid_queryparam(priority):
            problems = problems.filter(priority__icontains = priority)
        if is_valid_queryparam(impact):
            problems = problems.filter(impact__icontains = impact)
        if is_valid_queryparam(hardware_item):
            problems = problems.filter(hardware_item__name = hardware_item)
        if is_valid_queryparam(software_item):
            problems = problems.filter(software_item__name = software_item)
    

    context = { 'notification': notification, 'read_notification':read_notification, 'problems':problems }
    return render(request, 'problems/my_problems.html', context)






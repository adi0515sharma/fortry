from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Expenses
from .forms import ExpensesForm
from notifications.signals import notify
from django.contrib.auth.decorators import login_required, permission_required


@login_required
def Apply_Expenses(request):
    form = ExpensesForm()
    if request.method == 'POST':
        form = ExpensesForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.employee = request.user
            instance.save()
            notify.send(request.user, recipient=User.objects.filter(groups__name='HR'), verb='Expense application by %s'%(request.user), description="Expence" )
            return redirect('HR_tasks:dashboard')

    notification        =   request.user.notifications.unread()
    read_notification   =   request.user.notifications.read()
    context = { 'form':form, 
                'notification':notification, 
                'read_notification':read_notification}
    return render(request, 'HR_expenses/apply_expenses.html', context)


def is_valid_queryparam(param):
    return param != '' and param is not None


@login_required
@permission_required('HR_user_profiles.can_evaluate_all', raise_exception=True)
def list_expenses_admin(request):
    expense             =   Expenses.objects.all().filter(approved=None)
    user_list           =   User.objects.all()
    notification        =   request.user.notifications.unread()
    read_notification   =   request.user.notifications.read()

    if request.method  == 'GET' and request.GET.get('ordering_by')=='date_created' and request.GET.get('asddes')=='ascending':
        expense = expense.order_by('-created_on')
    if request.method  == 'GET' and request.GET.get('ordering_by') =='date_created' and request.GET.get('asddes')=='descending':
        expense = expense.order_by('created_on')
    if request.method  == 'GET' and request.GET.get('ordering_by')=='amount' and request.GET.get('asddes')=='ascending':
        expense = expense.order_by('-amount')
    if request.method  == 'GET' and request.GET.get('ordering_by') =='amount' and request.GET.get('asddes')=='descending':
        expense = expense.order_by('amount')

    if request.method =='GET' and 'filter' in request.GET:
        expense_title       =       request.GET.get('expense_title')
        employee_name       =       request.GET.get('employee_name')
        expense_greater     =       request.GET.get('expense_greater')
        expense_smaller     =       request.GET.get('expense_smaller')
        created_before      =       request.GET.get('created_before')

        if is_valid_queryparam(expense_title):
            expense = expense.filter(expense_on__icontains = expense_title)
        if is_valid_queryparam(employee_name):
            expense = expense.filter(employee__username = employee_name)
        if is_valid_queryparam(expense_greater):
            expense = expense.filter(amount__gte = expense_greater)
        if is_valid_queryparam(expense_smaller):
            expense = expense.filter(amount__lte = expense_smaller)
        if is_valid_queryparam(created_before):
            expense = expense.filter(created_on__lte = created_before)


    for exp in expense:
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



    context             =   {'notification'     :   notification, 
                             'read_notification':   read_notification, 
                             'expense'          :   expense,
                             'user_list'        :   user_list}
    return render(request, 'HR_expenses/adminview_expense.html', context)


@login_required
def my_Expence_list(request):
    expence             =       Expenses.objects.all().filter(employee=request.user).order_by('created_on')
    notification        =       request.user.notifications.unread()
    read_notification   =       request.user.notifications.read()
    context             =       {'expence'          :           expence,
                                 'notification'     :           notification,
                                 'read_notification':           read_notification}
    return render(request, 'HR_expenses/my_expence_list.html', context)


@login_required
@permission_required('HR_user_profiles.can_evaluate_all', raise_exception=True)
def detail_expense(request, pk):
    expence                 =       Expenses.objects.get(id = pk)
    notification            =       request.user.notifications.unread()
    read_notification       =       request.user.notifications.read()
    print(expence)
    context                 =       {   'expence'          :           expence,
                                        'notification'     :           notification,
                                        'read_notification':           read_notification}
    return render(request, 'HR_expenses/detail.html',context)


def employee_expence_total(request):
    

    users               =           User.objects.all()
    
    amount              =           0
    amount_list         =           []
    for u in users:
        expences            =           u.expenses_set.all()
        for exp in expences:
            amount         +=           exp.amount
        amount_list.append(amount)
        
    notification        =           request.user.notifications.unread()
    read_notification   =           request.user.notifications.read()
    context             =           {
                                    'users'             :           users,
                                    'amount_list'       :          amount_list,
                                    'notification'     :           notification,
                                    'read_notification':           read_notification,
                                    'amount'            :          amount
                                    }

    return render(request, 'HR_expenses/emp_total.html', context)

    

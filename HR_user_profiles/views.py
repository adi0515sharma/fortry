from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from django.views.generic import ListView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from .forms import ProfileUpdateForm, UserUpdateForm, UserCreateForm
from .models import Profile, Team


class EmployeeCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = User
    permission_required = 'HR_user_profiles.can_evaluate_all'
    form_class = UserCreateForm
    template_name = 'HR_user_profiles/create_user.html'
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['notification'] = self.request.user.notifications.unread()
        context['read_notification'] = self.request.user.notifications.read()
        return context

class EmployeeListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'HR_user_profiles.can_evaluate_all'
    model = User
    context_object_name = 'users'
    template_name = 'HR_user_profiles/user_list.html'

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
def team(request, user=None):
    if user is None:
        user = request.user
    else:
        if not request.user.has_perm('HR_user_profiles.can_evaluate_all') and user != request.user.username:
            return HttpResponse('<h2>You are not authorized to view this page</h2>')
        user = User.objects.get(username=user)
    if not user.profile.is_manager and Team.objects.filter(manager=user).exists():
        Team.objects.filter(manager=user).delete()

    if user.profile.is_manager and not Team.objects.filter(manager=user).exists():
        Team.objects.create(manager=user) 

    add_member = User.objects.filter(username=request.GET.get('add')).first()
    remove_member = User.objects.filter(username=request.GET.get('remove')).first()
    if add_member is not None:
        user.team.members.add(add_member)

    if remove_member is not None:
        user.team.members.remove(remove_member)
    notification = request.user.notifications.unread()
    read_notification = request.user.notifications.read()
    context = {
            'members': user.team.members.all(),
            'current_user': user,
            'users': User.objects.all(),
            'notification': notification,
            'read_notification':read_notification,
        }
    return render(request, "HR_user_profiles/team.html", context)

@login_required
def profile(request):
    if(request.method == 'POST'):
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, instance=request.user.profile)
        if(u_form.is_valid() and p_form.is_valid()):
            u_form.save()
            p_form.save()
            return redirect('HR_tasks:dashboard')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    notification = request.user.notifications.unread()
    read_notification = request.user.notifications.read()
    context = {
    'u_form': u_form,
    'p_form': p_form,
    'notification':notification,
    'read_notification':read_notification
    }
    return render(request, 'HR_user_profiles/profile.html', context)
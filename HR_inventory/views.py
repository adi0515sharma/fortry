from datetime import time
from django import forms
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
import datetime

from HR_problems.models import Prob_software
from .models import Hardware, Software, Vendor
from .forms import VendorForm


@login_required
@permission_required('HR_user_profiles.can_evaluate_all', raise_exception=True)
def inventory_home(request):
    notification =   request.user.notifications.unread()
    read_notification =   request.user.notifications.read()
    return render(request, 'HR_inventory/inventory_home.html', {'notification':notification, 'read_notification':read_notification})


class VendorListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'HR_user_profiles.can_evaluate_all'
    model = Vendor

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.method=='GET' and 'filter' in self.request.GET:
            vendor_name = self.request.GET.get('vendor_name')
            email = self.request.GET.get('email')
            contact_number = self.request.GET.get('contact_number')
            if vendor_name is not None:
                queryset = queryset.filter(name__icontains=vendor_name)
            if email is not None and email!='':
                queryset = queryset.filter(email__icontains=email)
            if contact_number is not None and contact_number!='':
                queryset = queryset.filter(number__icontains=contact_number)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['notification'] = self.request.user.notifications.unread()
        context['read_notification'] = self.request.user.notifications.read()
        return context



class VendorCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'HR_user_profiles.can_evaluate_all'
    model = Vendor
    fields = '__all__'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['notification'] = self.request.user.notifications.unread()
        context['read_notification'] = self.request.user.notifications.read()
        return context


class VendorUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'HR_user_profiles.can_evaluate_all'
    model = Vendor
    fields = '__all__'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['notification'] = self.request.user.notifications.unread()
        context['read_notification'] = self.request.user.notifications.read()
        return context


class VendorDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = 'HR_user_profiles.can_evaluate_all'
    model = Vendor
    success_url = '/HR/inventory/vendors'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['notification'] = self.request.user.notifications.unread()
        context['read_notification'] = self.request.user.notifications.read()
        return context


class HardwareListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'HR_user_profiles.can_evaluate_all'
    model = Hardware

    def get_queryset(self):
        queryset = super().get_queryset()
        ordering_by = self.request.GET.get('ordering_by')
        asddes = self.request.GET.get('asddes')
        if ordering_by is not None and asddes=='ascending':
            queryset = queryset.order_by('mfg_date')
        if ordering_by is not None and asddes=='descending':
            queryset = queryset.order_by('-mfg_date')


        if self.request.method=='GET' and 'filter' in self.request.GET:
            hardware_name = self.request.GET.get('hardware_name')
            item_type = self.request.GET.get('item_type')
            warranty_upto = self.request.GET.get('warranty_upto')
            mfg_date = self.request.GET.get('mfg_date')
            condition = self.request.GET.get('condition')
            user_name = self.request.GET.get('user_name')
            vendor_name = self.request.GET.get('vendor_name')
            if hardware_name is not None:
                queryset = queryset.filter(name__icontains=hardware_name)
            if item_type is not None:
                queryset = queryset.filter(item_type__icontains=item_type)
            if warranty_upto is not None and warranty_upto !='':
                queryset = queryset.filter(warranty__gte=warranty_upto)
            if mfg_date is not None and mfg_date !='':
                queryset = queryset.filter(mfg_date__gte=mfg_date)
            if condition is not None:
                queryset = queryset.filter(condition=condition)
            if user_name is not None:
                queryset = queryset.filter(users__username=user_name)
            if vendor_name is not None:
                queryset = queryset.filter(vendor__name=vendor_name)


        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users'] = User.objects.all()
        context['vendors'] = Vendor.objects.all()
        context['notification'] = self.request.user.notifications.unread()
        context['read_notification'] = self.request.user.notifications.read()
        return context


class HardwareCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'HR_user_profiles.can_evaluate_all'
    model = Hardware
    fields = '__all__'

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['mfg_date'].widget = forms.TextInput(attrs={'type': 'date'})
        form.fields['users'] = forms.ModelMultipleChoiceField(queryset=User.objects.all(),
                                                              widget=forms.SelectMultiple(
                                                              attrs={'class': 'selectpicker',
                                                                     'data-live-search': 'true',
                                                                     'data-size': '5',
                                                                     }
                                                              ))
        issue = self.request.POST.get('issue')
        if issue is not None and issue != '':
            p = Prob_software.objects.get(pk=issue)
            p.current_status = 'closed'
            p.save()
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['problems'] = Prob_software.objects.filter(current_status='active')
        context['notification'] = self.request.user.notifications.unread()
        context['read_notification'] = self.request.user.notifications.read()
        return context


class HardwareUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'HR_user_profiles.can_evaluate_all'
    model = Hardware
    fields = '__all__'

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['mfg_date'].widget = forms.TextInput(attrs={'type': 'date'})
        form.fields['users'] = forms.ModelMultipleChoiceField(queryset=User.objects.all(),
                                                              widget=forms.SelectMultiple(
                                                              attrs={'class': 'selectpicker',
                                                                     'data-live-search': 'true',
                                                                     'data-size': '5'
                                                                     }
                                                              ))
        issue = self.request.POST.get('issue')
        if issue is not None and issue != '':
            p = Prob_software.objects.get(pk=issue)
            p.current_status = 'closed'
            p.save()                                                    
        return form
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['problems'] = Prob_software.objects.filter(current_status='active')
        context['notification'] = self.request.user.notifications.unread()
        context['read_notification'] = self.request.user.notifications.read()
        return context


class HardwareDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = 'HR_user_profiles.can_evaluate_all'
    model = Hardware
    success_url = '/HR/inventory/hardwares'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['notification'] = self.request.user.notifications.unread()
        context['read_notification'] = self.request.user.notifications.read()
        return context


class SoftwareListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'HR_user_profiles.can_evaluate_all'
    model = Software

    def get_queryset(self):
        queryset = super().get_queryset()
        ordering_by = self.request.GET.get('ordering_by')
        asddes = self.request.GET.get('asddes')
        if ordering_by is not None and asddes=='ascending':
            queryset = queryset.order_by('start_date')
        if ordering_by is not None and asddes=='descending':
            queryset = queryset.order_by('-start_date')
        if ordering_by=="licensed_upto":
            queryset = queryset.order_by('end_date')

        if self.request.method=='GET' and 'filter' in self.request.GET:
            software_name = self.request.GET.get('software_name')
            item_type = self.request.GET.get('item_type')
            license_upto = self.request.GET.get('license_upto')
            mfg_date = self.request.GET.get('mfg_date')
            user_name = self.request.GET.get('user_name')
            vendor_name = self.request.GET.get('vendor_name')
            licensed = self.request.GET.get('licensed')
            print(licensed)
            if software_name is not None:
                queryset = queryset.filter(name__icontains=software_name)
            if item_type is not None:
                queryset = queryset.filter(item_type__icontains=item_type)
            if license_upto is not None and license_upto !='':
                queryset = queryset.filter(end_date__gte=license_upto)
            if mfg_date is not None and mfg_date !='':
                queryset = queryset.filter(mfg_date__gte=mfg_date)
            if user_name is not None:
                queryset = queryset.filter(users__username=user_name)
            if vendor_name is not None:
                queryset = queryset.filter(vendor__name=vendor_name)
            if licensed is not None and licensed =="on":
                queryset = queryset.filter(licensed=True)
            if licensed is not None and licensed =="off":
                queryset = queryset.filter(licensed=False)


        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users'] = User.objects.all()
        context['vendors'] = Vendor.objects.all()
        context['today'] = datetime.date.today()
        context['notification']  = self.request.user.notification.unread()
        context['read_notification'] = self.request.user.notifications.read()
        return context


class SoftwareCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'HR_user_profiles.can_evaluate_all'
    model = Software
    fields = '__all__'

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['start_date'].widget = forms.TextInput(attrs={'type': 'date'})
        form.fields['end_date'].widget = forms.TextInput(attrs={'type': 'date'})
        form.fields['users'] = forms.ModelMultipleChoiceField(queryset=User.objects.all(),
                                                              widget=forms.SelectMultiple(
                                                              attrs={'class': 'selectpicker',
                                                                     'data-live-search': 'true',
                                                                     'data-size': '5'
                                                                     }
                                                              ))
        issue = self.request.POST.get('issue')
        if issue is not None and issue != '':
            p = Prob_software.objects.get(pk=issue)
            p.current_status = 'closed'
            p.save()                                                      
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['problems'] = Prob_software.objects.filter(current_status='active')
        context['notification']  = self.request.user.notifications.unread()
        context['read_notification'] = self.request.user.notifications.read()
        return context


class SoftwareUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'HR_user_profiles.can_evaluate_all'
    model = Software
    fields = '__all__'

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['start_date'].widget = forms.TextInput(attrs={'type': 'date'})
        form.fields['end_date'].widget = forms.TextInput(attrs={'type': 'date'})
        form.fields['users'] = forms.ModelMultipleChoiceField(queryset=User.objects.all(),
                                                              widget=forms.SelectMultiple(
                                                              attrs={'class': 'selectpicker',
                                                                     'data-live-search': 'true',
                                                                     'data-size': '5'
                                                                     }
                                                              ))
        issue = self.request.POST.get('issue')
        if issue is not None and issue != '':
            p = Prob_software.objects.get(pk=issue)
            p.current_status = 'closed'
            p.save()                                                      
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['problems'] = Prob_software.objects.filter(current_status='active')
        context['notification']  = self.request.user.notification.unread()
        context['read_notification'] = self.request.user.notifications.read()
        return context


class SoftwareDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = 'HR_user_profiles.can_evaluate_all'
    model = Software
    success_url = '/HR/inventory/softwares'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['notification'] = self.request.user.notifications.unread()
        context['read_notification'] = self.request.user.notifications.read()
        return context


def VendorCreatePopup(request):
    form = VendorForm(request.POST or None)
    if form.is_valid():
        instance = form.save()

        return HttpResponse('<script>opener.closePopup(window, "%s", "%s", "#id_profile");</script>' % (instance.pk, instance))

    return render(request, "HR_inventory/Vendor_form_create.html", {"form": form})

def get_vendor_id(request):
    if request.is_ajax():
        vendor_name = request.GET['vendor_name']
        vendor_id = Vendor.objects.get(name= vendor_name).id
        data = {'vendor_id': vendor_id}
        return HttpResponse(json.dumps(data), content_type='application/json')
    return HttpResponse("/")

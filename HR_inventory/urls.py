from django.urls import path

import HR_inventory.views as inv_views

app_name = 'HR_inventory'

urlpatterns = [
    path('', inv_views.inventory_home, name='inventory-home'),

    path('vendors/', inv_views.VendorListView.as_view(), name='vendors'),
    path('vendor/create/', inv_views.VendorCreateView.as_view(), name='vendor-create'),
    path('vendor/<int:pk>/update/', inv_views.VendorUpdateView.as_view(), name='vendor-update'),
    path('vendor/<int:pk>/delete/', inv_views.VendorDeleteView.as_view(), name='vendor-delete'),

    path('hardwares/', inv_views.HardwareListView.as_view(), name='hardwares'),
    path('hardware/create/', inv_views.HardwareCreateView.as_view(), name='hardware-create'),
    path('hardware/<int:pk>/update/', inv_views.HardwareUpdateView.as_view(), name='hardware-update'),
    path('hardware/<int:pk>/delete/', inv_views.HardwareDeleteView.as_view(), name='hardware-delete'),
    path('vendor/create-new/', inv_views.VendorCreatePopup, name='VendorCreate'),
    path('vendor/ajax/get_vendor_id/', inv_views.get_vendor_id, name='get_vendor_id'),

    path('softwares/', inv_views.SoftwareListView.as_view(), name='softwares'),
    path('software/create/', inv_views.SoftwareCreateView.as_view(), name='software-create'),
    path('software/<int:pk>/update/', inv_views.SoftwareUpdateView.as_view(), name='software-update'),
    path('software/<int:pk>/delete/', inv_views.SoftwareDeleteView.as_view(), name='software-delete'),
]
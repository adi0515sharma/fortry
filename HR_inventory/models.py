from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.urls import reverse


def validate_number(number):
    if len(number) < 10:
        raise ValidationError("Enter a valid phone number")


class Vendor(models.Model):
    name = models.CharField(max_length=50, unique=True)
    number = models.CharField(max_length=14, unique=True, validators=[validate_number])
    email = models.EmailField(unique=True)
    address = models.CharField(max_length=200, blank=True, null=True)
    # created_on = models.DateTimeField(auto_now_add=True, auto_now=False)

    def get_absolute_url(self):
        return reverse('HR_inventory:vendors')

    def __str__(self):
        return self.name


class Hardware(models.Model):
    LAPTOP = 'L'
    KEYBOARD = 'K'
    MOUSE = 'M'
    ACCESSORY = 'A'
    SERVER = 'S'
    TYPE_CHOICES = [
        (LAPTOP, 'Laptop'),
        (KEYBOARD, 'Keyboard'),
        (MOUSE, 'Mouse'),
        (ACCESSORY, 'Accessory'),
        (SERVER, 'Server'),
    ]

    NEW = 'N'
    REFURBISHED = 'R'
    CONDITION_CHOICES = [
        (NEW, 'New'),
        (REFURBISHED, 'Refurbished'),
    ]

    name = models.CharField(max_length=100)
    quantity = models.IntegerField(validators=[MinValueValidator(1)])
    item_type = models.CharField(max_length=1, choices=TYPE_CHOICES)
    warranty = models.IntegerField(verbose_name='Warranty(in months)', validators=[MinValueValidator(0)])
    mfg_date = models.DateField()
    condition = models.CharField(max_length=1, choices=CONDITION_CHOICES)
    description = models.CharField(max_length=100)
    users = models.ManyToManyField(User, blank=True)
    vendor = models.ForeignKey(Vendor, null=True, on_delete=models.SET_NULL)
    # created_on = models.DateTimeField(auto_now_add=True, auto_now=False)

    def get_absolute_url(self):
        return reverse('HR_inventory:hardwares')

    def __str__(self):
        return self.name


class Software(models.Model):
    APPLICATION = 'A'
    OS = 'O'
    TYPE_CHOICES = [
        (APPLICATION, 'Application'),
        (OS, 'OS'),
    ]

    name = models.CharField(max_length=100)
    quantity = models.IntegerField(validators=[MinValueValidator(1)])
    item_type = models.CharField(max_length=1, choices=TYPE_CHOICES)
    start_date = models.DateField(verbose_name='License activation date')
    end_date = models.DateField(verbose_name='License expiration date', null=True, blank=True)
    licensed = models.BooleanField(default=False)
    description = models.CharField(max_length=100)
    users = models.ManyToManyField(User, blank=True)
    vendor = models.ForeignKey(Vendor, null=True, on_delete=models.SET_NULL)
    # created_on = models.DateTimeField(auto_now_add=True, auto_now=False)

    def get_absolute_url(self):
        return reverse('HR_inventory:softwares')

    def __str__(self):
        return self.name

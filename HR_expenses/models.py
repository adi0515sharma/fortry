from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth.models import User

class Expenses(models.Model):
    expense_on          =           models.CharField(max_length=30)
    description         =           models.TextField(max_length=250)
    amount              =           models.IntegerField(validators=[MinValueValidator(0)])
    employee            =           models.ForeignKey(User, on_delete=models.CASCADE)
    created_on          =           models.DateTimeField(auto_now=False, auto_now_add=True)
    approved            =           models.BooleanField(null=True)
    document            =           models.FileField(blank=True, upload_to='uploads/')

    def __str__(self):
        return str(self.employee) 
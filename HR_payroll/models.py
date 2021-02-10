from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator


class Salary(models.Model):
    employee = models.OneToOneField(User, on_delete=models.CASCADE)
    amount = models.IntegerField(validators=[MinValueValidator(0)], blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Salaries'

    def __str__(self):
        return self.employee.username + "'s Salary"

from django.db import models
from django.core.validators import MaxValueValidator
from django.contrib.auth.models import User
from HR_user_profiles.models import Profile

class WorkingDays(models.Model):
    january = models.IntegerField(validators=[MaxValueValidator(31)], null=True, blank=True)
    february = models.IntegerField(validators=[MaxValueValidator(29)], null=True, blank=True)
    march = models.IntegerField(validators=[MaxValueValidator(31)], null=True, blank=True)
    april = models.IntegerField(validators=[MaxValueValidator(30)], null=True, blank=True)
    may = models.IntegerField(validators=[MaxValueValidator(31)], null=True, blank=True)
    june = models.IntegerField(validators=[MaxValueValidator(30)], null=True, blank=True)
    july = models.IntegerField(validators=[MaxValueValidator(31)], null=True, blank=True)
    august = models.IntegerField(validators=[MaxValueValidator(31)], null=True, blank=True)
    september = models.IntegerField(validators=[MaxValueValidator(30)], null=True, blank=True)
    october = models.IntegerField(validators=[MaxValueValidator(31)], null=True, blank=True)
    november = models.IntegerField(validators=[MaxValueValidator(30)], null=True, blank=True)
    december = models.IntegerField(validators=[MaxValueValidator(31)], null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Working Days'

    def __str__(self):
        return 'Monthly Working Days'

class LeaveApplication(models.Model):
    title = models.CharField(max_length=30)
    reason = models.TextField(max_length=250)
    start = models.DateField()
    end = models.DateField()
    assign = models.ForeignKey(Profile, verbose_name='Assign work to', null=True, blank=True, on_delete=models.CASCADE)
    approved = models.BooleanField(null = True)
    employee = models.ForeignKey(User, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return self.title
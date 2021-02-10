from django.db import models
from django.urls import reverse
from datetime import datetime, timedelta, timezone, date
from django.core.exceptions import ValidationError
import pytz 
from django.contrib.auth.models import User
from datetime import datetime
from ckeditor.fields import RichTextField


def validate_date(date):
        if date < datetime.now(timezone.utc)-timedelta(days=2) or date > datetime.now(timezone.utc)+timedelta(days=2):
            raise ValidationError("Date can only be in 2 days period")




class Event(models.Model):

    COLOR_CHOICES = (
        ("ORANGE", "Orange"),
        ("GREEN", "Green"),
        ("YELLOW", "Yellow"),
        ("BLUE", "Blue"),
    )

    CALENDAR_CHOICES = (
        ("WORK", "Work"),
        ("PROJECT", "Project"),
    )

    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=200)
    start_time = models.DateTimeField(default=datetime.now(), validators=[validate_date])
    end_time = models.DateTimeField(default=datetime.now()+ timedelta(hours=1), validators=[validate_date])
    completed = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now=True, auto_now_add=False)
    color = models.CharField(max_length=9, default="ORANGE", choices=COLOR_CHOICES)
    calendar = models.CharField(max_length=9, default="WORK", choices=CALENDAR_CHOICES)
    # end_time = models.DateTimeField()

    def __str__(self):
        return self.title





WEEK_CHOICES = (
    ("1","1"),
    ("2","2"),
    ("3","3"),
    ("4","4"),
)

class Approval(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # approved = models.BooleanField(null=True)
    comment = RichTextField(default="Approved", max_length=250)
    year = models.CharField(max_length=120)
    month = models.CharField(max_length=120)
    week1 = models.BooleanField(null=True)
    week2 = models.BooleanField(null=True)
    week3 = models.BooleanField(null=True)
    week4 = models.BooleanField(null=True)
    date_created = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return str(self.user)


class Feedback(models.Model):
    type         =       models.CharField(max_length=50)
    description  =       models.TextField(max_length=500)

    def __str__(self):
        return self.type
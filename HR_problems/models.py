from django.db import models
from ckeditor.fields import RichTextField
from HR_inventory.models import Hardware, Software
from django.contrib.auth.models import User
from HR_user_profiles.models import Profile


PRIORITY_CHOICES = (
    ('low', 'low'),
    ('medium', 'medium'),
    ('high', 'high')
)

STATUS_CHOICES = (
    ('active', 'active'),
    ('closed', 'closed'),
    ('onGoing', 'onGoing')

)

IMPACT_CHOICES = (
    ('low', 'low'),
    ('high', 'high')
)


class Prob_software(models.Model):
    title = models.CharField(max_length=200)
    issue = RichTextField()
    solved = models.BooleanField(default=False)
    due_by = models.DateTimeField(auto_now_add=True, auto_now=False)
    priority = models.CharField(default='low', max_length=20, choices=PRIORITY_CHOICES)
    current_status = models.CharField(default='active', max_length=20, choices=STATUS_CHOICES)
    impact = models.CharField(default='low', max_length=20, choices=IMPACT_CHOICES)
    root_cause = models.CharField(max_length=200)
    Symptoms = models.CharField(max_length=200)
    hardware_item = models.ForeignKey(Hardware, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Hardware Related Item')
    software_item = models.ForeignKey(Software, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Software Related Item')
    # created_by = models.ForeignKey(Profile, verbose_name="Created BY", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return self.title

class Comment(models.Model):
    issue = models.ForeignKey(Prob_software, on_delete=models.CASCADE, related_name='comments')
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default='')
    
    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return 'Comment {} by {}'.format(self.body, self.user)

    
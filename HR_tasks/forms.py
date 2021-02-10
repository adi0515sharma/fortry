from django.forms import DateInput
from django import forms
from .models import Event, Approval

class EventForm(forms.ModelForm):
  class Meta:
    model = Event
    # datetime-local is a HTML5 input type, format to make date time show on fields
    widgets = {
      'date': DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
      # 'end_time': DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
    }
    fields = '__all__'
    exclude = ['user','calendar','color','approved']

  def __init__(self, *args, **kwargs):
    super(EventForm, self).__init__(*args, **kwargs)
    # input_formats parses HTML5 datetime-local input to datetime field
    self.fields['start_time'].input_formats = ('%Y-%m-%dT%H:%M',)
    # self.fields['end_time'].input_formats = ('%Y-%m-%dT%H:%M',)

class ApprovalForm(forms.ModelForm):
  def __init__(self, *args, **kwargs): 
        super(ApprovalForm, self).__init__(*args, **kwargs)
        self.fields['comment'].widget.attrs['rows'] = 2
  class Meta:
    model = Approval
    fields = ['comment', 'month']
    



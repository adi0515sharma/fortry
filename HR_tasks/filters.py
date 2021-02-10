from .models import Event
import django_filters
from django_filters import DateFilter

class EventFilter(django_filters.FilterSet):
    monthly_events = DateFilter(field_name="date", lookup_expr='gte')
    end_date = DateFilter(field_name="date", lookup_expr='lte' )
    class Meta:
        model = Event
        fields = ['monthly_events', 'end_date' ]
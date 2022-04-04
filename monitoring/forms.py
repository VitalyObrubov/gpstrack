from django.forms import ModelForm
from listenports.models import Trackers

class TrackerForm (ModelForm):
    class Meta:
        model = Trackers
        fields = ('user', 'tracker_id', 'description', 'resend')

from django.contrib import admin

# Register your models here.
from .models import Trackers, Tracks
admin.site.register(Trackers)
admin.site.register(Tracks)

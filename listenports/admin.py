from django.contrib import admin

# Register your models here.
from .models import Trackers, Tracks
class TrackersAdmin(admin.ModelAdmin) :
    list_display = ('tracker_id', 'description', 'user') 
    list_display_links = ('tracker_id',) 
    search_fields = ('user',)

admin.site.register(Trackers,TrackersAdmin)

class TracksAdmin(admin.ModelAdmin) :
    list_display = ('tracker_id', 'timestamp', 'lon', 'lat') 
    list_display_links = ('tracker_id',) 
    search_fields = ('tracker_id',)

admin.site.register(Tracks,TracksAdmin)

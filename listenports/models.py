from django.db import models

class Tracks(models.Model):
    tracker_id = models.IntegerField()
    lon = models.FloatField(null=True, blank=True)  
    lat = models.FloatField(null=True, blank=True)
    alt = models.FloatField(null=True, blank=True) 
    speed = models.FloatField(null=True, blank=True)
    accuracy = models.FloatField(null=True, blank=True)
    bearing = models.FloatField(null=True, blank=True)
    timestamp = models.DateTimeField()

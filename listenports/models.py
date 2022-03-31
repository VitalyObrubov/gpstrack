from django.db import models
from django.contrib.auth.models import User
class Trackers(models.Model):
    tracker_id = models.IntegerField(verbose_name='ИД трекера')
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, verbose_name='Пользователь') 
    description =  models.TextField(null=True, blank=True, verbose_name='Описание')
    resend = models.BooleanField(default=False, verbose_name='Переслать на livegpstracks.com') 
    class Meta:
        verbose_name_plural = 'Трекеры' 
        verbose_name = 'Трекер' 



class Tracks(models.Model):
    tracker_m = models.ForeignKey(Trackers, on_delete=models.DO_NOTHING, null=True, verbose_name='Трекер')
    tracker_id = models.IntegerField(verbose_name='ИД трекера')
    lon = models.FloatField(null=True, blank=True, verbose_name='Долгота')  
    lat = models.FloatField(null=True, blank=True, verbose_name='Широта')
    alt = models.FloatField(null=True, blank=True, verbose_name='Высота') 
    speed = models.FloatField(null=True, blank=True, verbose_name='Скорость')
    accuracy = models.FloatField(null=True, blank=True, verbose_name='Точность')
    bearing = models.FloatField(null=True, blank=True, verbose_name='Азимут')
    timestamp = models.DateTimeField(verbose_name='Время')
    class Meta:
        verbose_name_plural = 'Треки' 
        verbose_name = 'POI' 
    
 

from django.contrib import admin
from django.urls import path, include
from django.contrib.staticfiles.views import serve
from django.views.static import serve as media_serve

from django.conf import settings

from listenports.views import ListenPortView
from monitoring.views import IndexView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('sendgps/', ListenPortView.as_view(), name = 'sendgps'),
    path('monitoring/', include('monitoring.urls')),
    path('accounts/', include('monitoring.urls_acc')),
    path('ws/', include('websocket.urls')),
    path('media/<path:path>', media_serve,{'document_root':settings.MEDIA_ROOT}),
    path ('static/<path:path>', serve,{'insecure': True}),
    path('', IndexView.as_view(), name = 'index'),
]


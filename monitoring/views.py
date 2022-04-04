from django.shortcuts import render
from django.http import HttpResponse, HttpResponseForbidden
from django.views.generic.base import View
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy



from listenports.models import Trackers
from .forms import TrackerForm

class IndexView(View):
    def post(self, request):
        return HttpResponse()

    def get(self, request):
        return render(request, 'monitoring/index.html')

class TrackerCreateView(CreateView):
    template_name = 'monitoring/create_tracker.html' 
    form_class = TrackerForm 
    success_url = reverse_lazy('monitoring')

    def get_context_data(self, **kwargs): 
        context = super().get_context_data(**kwargs) 
        context['trackers'] = Trackers.objects.all() 
        return context

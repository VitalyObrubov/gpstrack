from django.shortcuts import render
from django.http import HttpResponse, HttpResponseForbidden
from django.views.generic.base import View
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.views.generic.base import TemplateView
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin


from .forms import RegisterUserForm, ProfileForm



from listenports.models import Trackers
from .forms import TrackerForm

class IndexView(View):
    def post(self, request):
        return HttpResponse()

    def get(self, request):
        return render(request, 'monitoring/index.html')

class MonitoringView(LoginRequiredMixin, View):
    def post(self, request):
        return HttpResponse()

    def get(self, request):
        context={}
        trackers = []
        for tracker in request.user.trackers_set.all():
            tracker_d = {}
            tracker_d["tracker"] = tracker
            tracker_d["pos"] = tracker.tracks.last()
            tracker_d["track"] = tracker.tracks.all()
            trackers.append(tracker_d)

        context["trackers"] = trackers    


        return render(request, 'monitoring/monitoring.html', context)
        

class TrackerCreateView(LoginRequiredMixin, CreateView):
    template_name = 'monitoring/create_tracker.html' 
    form_class = TrackerForm 
    success_url = reverse_lazy('monitoring')

@login_required
def profile(request):
    return render(request, 'registration/profile.html')

class ProfileView(LoginRequiredMixin, View):
    form_class = ProfileForm 
    def post(self, request):
        return HttpResponse()

    def get(self, request,**kwargs):
        context = {}
         # super().get_context_data(**kwargs) 
        context['trackers'] = request.user.trackers_set.all()
        return render(request, 'registration/profile.html',context)


class RegisterUserView(CreateView):
    model = User
    template_name = 'registration/register_user.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('register_done')


class RegisterDoneView(TemplateView):
    template_name = 'registration/register_done.html'
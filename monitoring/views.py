from django.shortcuts import render
from django.forms import inlineformset_factory
from django.http import HttpResponse, HttpResponseForbidden
from django.views.generic.base import View
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.views.generic.base import TemplateView
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin

import json
from typing import List, Dict
from dataclasses import asdict

from .forms import RegisterUserForm, ProfileForm, TrackerForm
from listenports.models import Trackers


class IndexView(View):
    def post(self, request):
        return HttpResponse()

    def get(self, request):
        return render(request, 'monitoring/index.html')

class MonitoringView(LoginRequiredMixin, View):
    def post(self, request):
        return HttpResponse()

    def get(self, request):
        context = {}
        context['trackers'] = request.user.trackers_set.all()
        return render(request, 'monitoring/monitoring.html',context)
        

class TrackerCreateView(LoginRequiredMixin, CreateView):
    template_name = 'monitoring/create_tracker.html' 
    form_class = TrackerForm
    success_url = reverse_lazy('monitoring')


class ProfileView(LoginRequiredMixin, View):
    form_class = ProfileForm 
    def post(self, request):
        TrackersFormSet = inlineformset_factory(User, Trackers, fields = "__all__", extra = 1)
        formset = TrackersFormSet(request.POST, instance=request.User)
        if formset.is_valid():
            formset.save()
            context = {"formset:formset"}
            return render(request, 'registration/profile.html', context)


    def get(self, request,**kwargs):
        TrackersFormSet = inlineformset_factory(User, Trackers, fields = "__all__", extra = 1) 
        formset = TrackersFormSet(instance=request.User)

        context = {"formset:formset"}
        return render(request, 'registration/profile.html', context)


class RegisterUserView(CreateView):
    model = User
    template_name = 'registration/register_user.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('register_done')


class RegisterDoneView(TemplateView):
    template_name = 'registration/register_done.html'
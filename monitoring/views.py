from django.shortcuts import render
from django.forms import inlineformset_factory
from django.http import HttpResponse
from django.views.generic.base import View
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.views.generic.base import TemplateView
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import RegisterUserForm, TrackerForm, ChangeUserInfoForm
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
        return render(request, 'monitoring/monitoring.html', context)


class ProfileView(LoginRequiredMixin, View):
    def post(self, request):
        user_form = ChangeUserInfoForm(request.POST, instance=request.user)
        if request.user.is_staff:
            TrackersFormSet = inlineformset_factory(User, Trackers, form=TrackerForm,
                                                    fields="__all__", extra=1)
        else:
            TrackersFormSet = inlineformset_factory(User, Trackers, form=TrackerForm,
                                                    fields=("tracker_id", "description",), extra=1)
        formset = TrackersFormSet(request.POST, instance=request.user)
        if formset.is_valid() and user_form.is_valid():
            formset.save()
            user_form.save()
            context = {"formset": formset,
                       "user_form": user_form,
                       }
            return render(request, 'registration/profile.html', context)

    def get(self, request, **kwargs):
        user_form = ChangeUserInfoForm(instance=request.user)
        if request.user.is_staff:
            TrackersFormSet = inlineformset_factory(User, Trackers, form=TrackerForm,
                                                    fields="__all__", extra=1)
        else:
            TrackersFormSet = inlineformset_factory(User, Trackers, form=TrackerForm,
                                                    fields=("tracker_id", "description",), extra=1)
        formset = TrackersFormSet(instance=request.user)

        context = {"formset": formset,
                   "user_form": user_form,
                   }
        return render(request, 'registration/profile.html', context)


class RegisterUserView(CreateView):
    model = User
    template_name = 'registration/register_user.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('register_done')


class RegisterDoneView(TemplateView):
    template_name = 'registration/register_done.html'

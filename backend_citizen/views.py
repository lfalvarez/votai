# coding=utf-8
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView
from popular_proposal.forms import ProposalTemporaryDataUpdateForm
from popular_proposal.models import (ProposalTemporaryData,
                                     PopularProposal,
                                     ProposalLike)
from django.urls import reverse
from django.views.generic.edit import UpdateView
from backend_citizen.forms import (UserChangeForm,
                                   GroupCreationForm)
from django.contrib.auth.models import User
from backend_citizen.models import Profile
from django.views.generic.edit import CreateView
from django_registration.backends.activation.views import RegistrationView
from django.views.generic.list import ListView
from backend_citizen.stats import StatsPerProposal, PerUserTotalStats
from django.views.generic.base import RedirectView
from backend_candidate.models import is_candidate
from agenda.forms import ActivityForm
from agenda.models import Activity
from django.contrib.contenttypes.models import ContentType
from votai_utils.send_mails import send_mail


class IndexView(LoginRequiredMixin, RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        if is_candidate(self.request.user):
            candidacy = self.request.user.candidacies.first()
            return reverse('backend_candidate:complete_profile',
                                         kwargs={'slug': candidacy.candidate.election.slug,
                                                 'candidate_slug': candidacy.candidate.slug})
        if self.request.user.profile.is_organization:
            return reverse('organization_profiles:update')
        return reverse('backend_citizen:update_my_profile')

class MyProposalsView(LoginRequiredMixin, TemplateView):
    template_name = 'backend_citizen/my_proposals.html'

    def get_context_data(self, **kwargs):
        context = super(MyProposalsView, self).get_context_data(**kwargs)
        context['temporary_proposals'] = ProposalTemporaryData.objects.filter(proposer=self.request.user).order_by('-updated')
        return context


class PopularProposalTemporaryDataUpdateView(LoginRequiredMixin, FormView):
    template_name = 'backend_citizen/temporary_data_update.html'
    form_class = ProposalTemporaryDataUpdateForm

    def get_form_kwargs(self):
        kwargs = super(PopularProposalTemporaryDataUpdateView, self).get_form_kwargs()
        pk = self.kwargs.pop('pk')
        self.temporary_data = ProposalTemporaryData.objects.get(id=pk)
        kwargs['temporary_data'] = self.temporary_data
        kwargs['proposer'] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(PopularProposalTemporaryDataUpdateView, self).get_context_data(**kwargs)
        context['temporary_data'] = self.temporary_data
        return context

    def get_success_url(self):
        return reverse('backend_citizen:my_proposals')

    def form_valid(self, form):
        form.save()
        return super(PopularProposalTemporaryDataUpdateView, self).form_valid(form)


class UpdateUserView(LoginRequiredMixin, UpdateView):
    form_class = UserChangeForm
    model = User
    template_name = 'backend_citizen/update_my_profile.html'

    def get_object(self):
        return self.request.user

    def get_success_url(self):
        return reverse('backend_citizen:index')

class UpdateSubscription(UpdateView):
    model = Profile
    template_name = 'backend_citizen/update_subscription.html'
    slug_url_kwarg = 'token'
    slug_field = 'unsubscribe_token'
    fields = ['unsubscribed',]

    def get_success_url(self):
        return reverse('backend_citizen:already_unsuscribed',
                        kwargs={'token': self.object.unsubscribe_token})


class AlreadyUnsubscribed(DetailView):
    model = Profile
    template_name = 'backend_citizen/already_unsuscribed.html'
    slug_url_kwarg = 'token'
    slug_field = 'unsubscribe_token'


class GroupRegistrationView(RegistrationView):
    form_class = GroupCreationForm

    def register(self, form):
        new_user = super(GroupRegistrationView, self).register(form)
        return new_user

    def get_success_url(self, user):
        return reverse('django_registration_activation_complete')

    def create_inactive_user(self, form):
        group = super(GroupRegistrationView, self).create_inactive_user(form)
        form.set_group_profile(group)
        return group

    def send_activation_email(self, user):
        """
        Send the activation email. The activation key is the username,
        signed using TimestampSigner.
        """
        activation_key = self.get_activation_key(user)
        context = self.get_email_context(activation_key)
        context.update({
            'user': user,
        })
        send_mail(context, 'organization_activation', to=[user.email],)


class MySupportsView(LoginRequiredMixin, ListView):
    template_name = 'backend_citizen/my_supports.html'
    model = ProposalLike
    context_object_name = 'supports'

    def get_queryset(self):
        qs = super(MySupportsView, self).get_queryset()
        qs = qs.filter(user=self.request.user)
        return qs


class MyStats(LoginRequiredMixin, TemplateView):
    template_name = 'backend_citizen/stats.html'

    def get_context_data(self, **kwargs):
        context = super(MyStats, self).get_context_data(**kwargs)
        stats = {}
        proposals = PopularProposal.objects.filter(proposer=self.request.user)
        for proposal in proposals:
            stats[proposal.id] = StatsPerProposal(proposal)
        context['stats'] = stats
        context['total_stats'] = PerUserTotalStats(self.request.user)
        return context


class AddActivityToUserView(LoginRequiredMixin, CreateView):
    form_class = ActivityForm
    template_name = 'backend_citizen/add_activity.html'

    def get_success_url(self):
        return reverse('backend_citizen:all_my_activities')

    def get_form_kwargs(self):
        kwargs = super(AddActivityToUserView, self).get_form_kwargs()
        kwargs['content_object'] = self.request.user
        return kwargs


class ActivityListView(ListView):
    model = Activity
    context_object_name = 'activities'
    def get_queryset(self):
        content_type = ContentType.objects.get_for_model(User)
        return Activity.objects.filter(content_type=content_type)


class MyActivitiesListView(LoginRequiredMixin, ActivityListView):
    template_name = 'backend_citizen/all_my_activities.html'

    def get_queryset(self):
        qs = super(MyActivitiesListView, self).get_queryset()
        return qs.filter(object_id=self.request.user.id)


class AllActivitiesListView(ActivityListView):
    template_name = 'agenda/all_activities.html'

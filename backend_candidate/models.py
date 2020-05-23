from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from elections.models import Candidate
import uuid
from votai_utils.send_mails import send_mail
from django.urls import reverse
from django.contrib.sites.models import Site
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
import time


class Candidacy(models.Model):
    user = models.ForeignKey(User, related_name='candidacies', on_delete=models.CASCADE)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True,
                                   blank=True,
                                   null=True)
    updated = models.DateTimeField(auto_now=True,
                                   blank=True,
                                   null=True)


    def get_complete_profile_url(self):
        url = reverse('backend_candidate:complete_profile',
                              kwargs={'slug': self.candidate.election.slug,
                              'candidate_slug': self.candidate.slug})
        return url


def is_candidate(user):
    if not user.is_authenticated:
        return False
    if user.candidacies.count():
        return True
    return False

def send_candidate_a_candidacy_link(candidate):
    if not settings.NOTIFY_CANDIDATES:
        return
    if candidate.contacts.filter(used_by_candidate=True):
        return
    for contact in candidate.contacts.all():
        contact.send_mail_with_link()


def send_candidate_username_and_password(candidate):
    if not settings.NOTIFY_CANDIDATES:
        return
    if candidate.contacts.filter(used_by_candidate=True):
        return
    for contact in candidate.contacts.all():
        contact.send_mail_with_user_and_password()

def add_contact_and_send_mail(mail, candidate):
    contact = CandidacyContact.objects.create(mail=mail,
                                              candidate=candidate)
    send_candidate_username_and_password(candidate)
    for candidacy in candidate.candidacy_set.all():
        candidacy.user.email = mail
        candidacy.user.save()


def unite_with_candidate_if_corresponds(user):
    if not user.email:
        return
    try:
        contacts = CandidacyContact.objects.filter(mail=user.email)
        for contact in contacts:
            if not Candidacy.objects.filter(user=user, candidate=contact.candidate).exists():
                Candidacy.objects.create(user=user, candidate=contact.candidate)
    except CandidacyContact.DoesNotExist as e:
        return


class CandidacyContact(models.Model):
    candidate = models.ForeignKey(Candidate, related_name='contacts', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='candidacy_contact', null=True, on_delete=models.CASCADE)
    mail = models.EmailField()
    times_email_has_been_sent = models.IntegerField(default=0)
    used_by_candidate = models.BooleanField(default=False)
    identifier = models.UUIDField(default=uuid.uuid4)
    candidacy = models.ForeignKey(Candidacy,
                                  null=True,
                                  blank=True,
                                  on_delete=models.CASCADE,
                                  default=None)
    initial_password = models.CharField(max_length=255,
                                        blank=True)

    def send_mail_with_link(self):
        if self.times_email_has_been_sent >= settings.MAX_AMOUNT_OF_MAILS_TO_CANDIDATE:
            return
        send_mail({'contact': self}, 'candidates/join_us_pls', to=[self.mail],)
        self.times_email_has_been_sent += 1
        self.save()

    def set_initial_password(self):
        password = uuid.uuid4().hex[:12]
        self.initial_password = password

    def create_and_set_user(self):
        username = self.candidate.slug[:20] + str(uuid.uuid4())[:4]
        print(username)
        self.set_initial_password()
        user = User.objects.create(username=username)
        user.set_password(self.initial_password)
        user.email = self.mail
        user.save()
        self.candidacy = Candidacy.objects.create(user=user, candidate=self.candidate)
        self.user = user
        self.save()
        return user


    def send_mail_with_user_and_password(self):
        if self.times_email_has_been_sent >= settings.MAX_AMOUNT_OF_MAILS_TO_CANDIDATE:
            return
        self.times_email_has_been_sent += 1
        if self.candidacy is None:
            user = self.create_and_set_user()

        site = Site.objects.get_current()
        login_url = reverse('backend_candidate:candidate_auth_login')
        full_login_url = "http://%s%s" % (site.domain, login_url)
        send_mail({'contact': self, 'login_url': full_login_url},
                  'candidates/mail_with_user_and_password', to=[self.mail],)


    def get_absolute_url(self):
        site = Site.objects.get_current()
        path = reverse('backend_candidate:candidacy_user_join',
                       kwargs={'identifier': self.identifier.hex})
        return "http://%s%s" % (site.domain, path)

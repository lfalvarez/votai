from django.urls import path

from suggestions_for_candidates.views import (CandidateIncrementalDetailView,
                                              )
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('commit_to_suggestions/<str:identifier>',
         csrf_exempt(CandidateIncrementalDetailView.as_view()),
         name='commit_to_suggestions'),
]

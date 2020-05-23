from django.conf import settings
from django.urls import re_path, path

from haystack.views import SearchView
from elections.forms import ElectionForm
from elections.views import (
    ElectionsSearchByTagView,
    HomeView,
    ElectionDetailView,
    CandidateDetailView,
    FaceToFaceView,
    AreaDetailView,
    KnowYourCandidatesView,
)

from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.decorators.cache import cache_page

media_root = getattr(settings, 'MEDIA_ROOT', '/')

urlpatterns = [
    path('', cache_page(60 * settings.CACHE_MINUTES)(xframe_options_exempt(HomeView.as_view())), name='home'),
    path('buscar', SearchView(template='search.html',
                                      form_class=ElectionForm), name='search'),
    path('busqueda_tags', ElectionsSearchByTagView.as_view(), name='tags_search'),
    path('eleccion/<slug:slug>',
                ElectionDetailView.as_view(template_name='elections/election_detail.html'),
            name='election_view'),
    path('eleccion/<slug:slug>/questionary',
                ElectionDetailView.as_view(template_name='elections/election_questionary.html'),
            name='questionary_detail_view'),
    # compare two candidates
    path('eleccion/<slug:slug>/face-to-face/<slug:slug_candidate_one>/<slug:slug_candidate_two>',
                FaceToFaceView.as_view(template_name='elections/compare_candidates.html'),
            name='face_to_face_two_candidates_detail_view'),
    # one candidate for compare
    path('eleccion/<slug:slug>/face-to-face/<slug:slug_candidate_one>',
                ElectionDetailView.as_view(template_name='elections/compare_candidates.html'),
            name='face_to_face_one_candidate_detail_view'),
    # no one candidate
    path('eleccion/<slug:slug>/face-to-face',
                ElectionDetailView.as_view(template_name='elections/compare_candidates.html'),
            name='face_to_face_no_candidate_detail_view'),

    path('eleccion/<slug:election_slug>/<slug:slug>',
                CandidateDetailView.as_view(template_name='elections/candidate_detail.html'),
            name='candidate_detail_view'
            ),
    path('candidaturas/<slug:area_slug>/<slug:slug>',
            cache_page(60 * settings.CACHE_MINUTES)(
                CandidateDetailView.as_view(template_name='elections/candidate_detail.html')),
            name='candidate_detail_view_area'
            ),
    path('eleccion/<slug:slug>/extra_info.html',
            ElectionDetailView.as_view(template_name='elections/extra_info.html'),
            name='election_extra_info'),
    path('candidaturas/<slug>',
            AreaDetailView.as_view(template_name='elections/area.html'),
            name='area'),
    path('ayudanos/<slug>',
            ElectionDetailView.as_view(template_name='elections/ayudanos.html'),
            name='help_election'),
    path('candidaturas', KnowYourCandidatesView.as_view(), name='know_your_candidates'),
]

# urlpatterns += [
#     re_path(r'^cache/(?P<path>.*)$', sitemap,
#         {'document_root': media_root})
# ]

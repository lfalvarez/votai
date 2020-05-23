from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path, include
from django.contrib.auth.views import LoginView
from votainteligente.rest_api_router import router
from django.conf import settings
from django.conf.urls.static import static

from backend_candidate.views import HelpFindingCandidates

urlpatterns = [
    path('', include('elections.urls')),
    path('propuestas/', include(('popular_proposal.urls', 'popular_proposal'), namespace='popular_proposals')),
    path('perfil_ciudadano/', include(('backend_citizen.urls', 'backend_citizen'), namespace='backend_citizen')),
    path('organizacion/',
         include(('organization_profiles.urls', 'organization_profiles'), namespace='organization_profiles')),
    path('candidatos/', include(('backend_candidate.urls', 'backend_candidate'), namespace='backend_candidate')),
    path('backend_staff/', include(('backend_staff.urls', 'backend_staff'), namespace='backend_staff')),

    path('media_naranja', include(('medianaranja2.urls', 'medianaranja2'), namespace='medianaranja2')),
    path('proposal_subscriptions', include(('proposal_subscriptions.urls', 'proposal_subscriptions'), namespace='proposal_subscriptions')),
    path('suggestions/', include(('suggestions_for_candidates.urls', 'suggestions_for_candidates'), namespace='suggestions_for_candidates')),
    path('ayudanos/',
         HelpFindingCandidates.as_view(),
         name='help'),
    path('social', include(('social_django.urls', 'social_django'), namespace='social')),
    path('admin/', admin.site.urls),
    path('accounts/', include('django_registration.backends.activation.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/login/organizacion',
         LoginView.as_view(template_name='django_registration/login_organizacion.html'),
         name='login_users'),
    path('accounts/login/usuario_y_password',
         LoginView.as_view(template_name='django_registration/login_username_and_password.html'),
         name='username_and_password'),
    path('api/', include(router.urls)),
]
urlpatterns += staticfiles_urlpatterns()
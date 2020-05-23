from django.urls import path
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from medianaranja2.views import (ShareYourResult,
                                 ShareMyResultPlz,
                                 ShareMyResultOrgPlz,
                                 SharedResultOGImageView,
                                 get_medianaranja_view)
from django.utils.translation import ugettext_lazy as _


urlpatterns = [
    path('',
        get_medianaranja_view,
        name='index'),
    path('compartir',
        ShareMyResultPlz.as_view(),
        name='create_share'),
    path('compartir_org',
        ShareMyResultOrgPlz.as_view(),
        name='create_share_org'),
    path('compartir/<str:identifier>',
        ShareYourResult.as_view(),
        name='share'),
    path('og_image/<str:identifier>.jpg',
        SharedResultOGImageView.as_view(),
        name='og_image'),
]
if settings.DEBUG:# pragma: no cover
    from medianaranja2.forms import MediaNaranjaResultONLYFORDEBUG
    urlpatterns += [
        path('medianaranja2_resultado/', MediaNaranjaResultONLYFORDEBUG.as_view(),
        name='medianaranja2_resultado')
    ]

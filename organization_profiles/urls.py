from django.urls import path
from organization_profiles.views import (OrganizationDetailView,
                                         OrganizationTemplateUpdateView,
                                         AyuranosView,
                                         OrganizationListView,
                                         OrganizationTemplateOGPImage,
                                         ExtraPageUpdateView)


urlpatterns = [
    path('', OrganizationListView.as_view(), name='index'),
    path('update/extra_pages/<int:pk>', ExtraPageUpdateView.as_view(), name='update_extrapage'),
    path('update', OrganizationTemplateUpdateView.as_view(), name='update'),
    path('<slug:slug>',
        OrganizationDetailView.as_view(),
        name='home'),
    path('<slug:slug>/ayudanos',
        AyuranosView.as_view(),
        name='ayuranos'),
    path('og_image/<slug:slug>.jpg',
        OrganizationTemplateOGPImage.as_view(),
        name='og_image'),
]

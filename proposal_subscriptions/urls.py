from django.urls import path
from proposal_subscriptions.views import (SearchSubscriptionCreateView,
                                          SearchSubscriptionListView,
                                          SearchSubscriptionDeleteView)

urlpatterns = [
    path('subscribe',
        SearchSubscriptionCreateView.as_view(),
        name='subscribe'),
    path('unsubscribe/<str:token>',
        SearchSubscriptionDeleteView.as_view(),
        name='unsubscribe'),
    path('unsubscribe',
        SearchSubscriptionListView.as_view(),
        name='list'),
]

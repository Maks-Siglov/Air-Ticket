from django.urls import path

from flight.api.v1 import views

app_name = "api-flight"

urlpatterns = [
    path(
        "search-flights/", views.SearchFlightsAPIView.as_view(), name="search"
    ),
    path(
        "suggest-city/<str:value>/",
        views.SuggestAirportAPIView.as_view(),
        name="suggest-city",
    ),
]

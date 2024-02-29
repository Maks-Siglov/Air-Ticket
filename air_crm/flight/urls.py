from django.urls import path

from flight import views

app_name = "flight"

urlpatterns = [
    path("search-flights/", views.search_flights, name="search"),
]

from django.urls import path

from booking import views

app_name = "booking"

urlpatterns = [
    path("book/<int:flight_pk>", views.book, name="book"),
    path(
        "create-ticket/<int:flight_pk>",
        views.create_ticket,
        name="create_ticket"
    ),
]

from django.urls import path

from booking import views

app_name = "booking"

urlpatterns = [
    path(
        "order/<int:flight_pk>",
        views.create_order,
        name="create_order",
    ),
    path("book/<int:order_pk>", views.book, name="book"),
    path(
        "create-ticket/<int:flight_pk>",
        views.create_ticket,
        name="create_ticket",
    ),
    path(
        "update-ticket/<int:ticket_pk>",
        views.update_ticket,
        name="update_ticket",
    ),
    path("create-contact/", views.create_contact, name="create_contact"),
    path(
        "update-contact/<int:contact_pk>",
        views.update_contact,
        name="update_contact",
    ),
]

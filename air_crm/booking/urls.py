from django.urls import path

from booking import views

app_name = "booking"

urlpatterns = [
    path(
        "preorder/<int:flight_pk>",
        views.create_preorder,
        name="create_preorder",
    ),
    path("book/<int:preorder_pk>", views.book, name="book"),
    path(
        "create-ticket/<int:flight_pk>",
        views.create_ticket,
        name="create_ticket",
    ),
    path("checkout/<int:ticket_pk>", views.checkout, name="checkout"),
    path(
        "create-checkout-session/<int:ticket_pk>",
        views.create_checkout_session,
        name="create_checkout_session",
    ),
    path("session-status/", views.session_status, name="session_status"),
    path(
        "<int:ticket_pk>/return/",
        views.checkout_return,
        name="checkout_return",
    )
]

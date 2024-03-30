from django.urls import path

from booking.api.v1 import views

app_name = "api-booking"

urlpatterns = [
    path(
        "create-ticket/<int:cart_pk>/",
        views.TicketAPI.as_view(),
        name="create_ticket",
    ),
    path(
        "update-ticket/<int:ticket_pk>/",
        views.TicketAPI.as_view(),
        name="update_ticket",
    ),
]

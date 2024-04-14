from django.urls import path

from booking.api.v1 import views

app_name = "api-booking"

urlpatterns = [
    path(
        "create-ticket/<int:cart_pk>/",
        views.CreateTicketCartAPI.as_view(),
        name="create_ticket",
    ),
    path(
        "update-ticket/<int:ticket_pk>/",
        views.TicketUpdateAPI.as_view(),
        name="update_ticket",
    ),
    path(
        "create-contact/<int:cart_pk>/",
        views.CreateContactAPI.as_view(),
        name="create_contact",
    ),
    path(
        "update-contact/<int:contact_pk>/",
        views.UpdateContactAPI.as_view(),
        name="update_contact",
    ),
    path(
        "delete-expired-bookings/",
        views.DeleteExpiredBookingAPI.as_view(),
        name="delete_expired_bookings",
    ),
]

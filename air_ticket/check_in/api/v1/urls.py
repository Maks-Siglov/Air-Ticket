from django.urls import path

from check_in.api.v1 import views

app_name = "api-check-in"

urlpatterns = [
    path("<int:flight_pk>", views.SeatsView.as_view(), name="get_seats"),
    path(
        "select-seat/<int:seat_pk>/<int:order_ticket_pk>",
        views.SelectSeatView.as_view(),
        name="select_seat",
    ),
    path(
        "decline-seat/<int:seat_pk>",
        views.DeclineSeatView.as_view(),
        name="decline_seat",
    ),
]

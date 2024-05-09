from django.urls import path

from check_in.api.v1 import views

app_name = "api-check-in"

urlpatterns = [
    path(
        "select-seat/<int:seat_number>/ticket/<int:order_ticket_pk>",
        views.SelectSeatView.as_view(),
        name="select_seat",
    ),
    path(
        "decline-seat/<int:seat_number>/order/<int:order_pk>",
        views.DeclineSeatView.as_view(),
        name="decline_seat",
    ),
]

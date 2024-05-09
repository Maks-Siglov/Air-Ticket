from django.urls import path

from booking import views

app_name = "booking"

urlpatterns = [
    path(
        "order/<int:flight_pk>",
        views.create_cart,
        name="create_order",
    ),
    path("book/<int:cart_pk>", views.book, name="book"),
]

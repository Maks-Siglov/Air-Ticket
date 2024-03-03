from django.urls import path

from orders import views

app_name = "orders"

urlpatterns = [
    path("book/<int:flight_pk>", views.book, name="book"),
]

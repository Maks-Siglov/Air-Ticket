from django.urls import path

from customer import views

app_name = "customer"

urlpatterns = [
    path("profile/", views.profile, name="profile"),
    path("orders/", views.customer_orders, name="orders"),
    path("flights/", views.customer_flights, name="flights"),
    path("check-in/", views.customer_check_ins, name="check-in"),
]

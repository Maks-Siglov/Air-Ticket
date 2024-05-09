from django.urls import path

from orders import views

app_name = "orders"

urlpatterns = [
    path("checkout/<int:cart_pk>", views.checkout, name="checkout"),
    path(
        "create-checkout-session/<int:order_pk>",
        views.create_checkout_session,
        name="create_checkout_session",
    ),
    path("session-status/", views.session_status, name="session_status"),
    path(
        "<int:order_pk>/return/",
        views.checkout_return,
        name="checkout_return",
    ),
    path(
        "<int:order_pk>/detail/",
        views.order_details,
        name="detail",
    ),
]

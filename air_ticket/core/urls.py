"""
URL configuration for air_ticket project.
"""

from django.conf import settings
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("main.urls", namespace="main")),
    path("users/", include("users.urls", namespace="users")),
    path("customer/", include("customer.urls", namespace="customer")),
    path("flight/", include("flight.urls", namespace="flight")),
    path("booking/", include("booking.urls", namespace="booking")),
    path("orders/", include("orders.urls", namespace="orders")),
]

if settings.DEBUG:
    urlpatterns += [
        path("__debug__/", include("debug_toolbar.urls")),
    ]

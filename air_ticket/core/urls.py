"""
URL configuration for air_ticket project.
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("main.urls", namespace="main")),
    path("users/", include("users.urls", namespace="users")),
    path("customer/", include("customer.urls", namespace="customer")),
    path("flight/", include("flight.urls", namespace="flight")),
    path("api/v1/flights/", include("flight.api.v1.urls")),
    path("booking/", include("booking.urls", namespace="booking")),
    path("api/v1/booking/", include("booking.api.v1.urls")),
    path("orders/", include("orders.urls", namespace="orders")),
    path("check-in/", include("check_in.urls", namespace="check_in")),
    path("api/v1/check-in/", include("check_in.api.v1.urls")),
]

if settings.DEBUG:
    urlpatterns += [
        path("__debug__/", include("debug_toolbar.urls")),
    ]

    media_urls = static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += media_urls

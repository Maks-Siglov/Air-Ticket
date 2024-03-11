from django.urls import path

from check_in import views

app_name = "check_in"

urlpatterns = [
    path("<int:flight_pk>", views.check_in, name="check_in")
]

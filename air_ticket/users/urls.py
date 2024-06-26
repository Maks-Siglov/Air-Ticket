from django.urls import path

from users import views

app_name = "users"

urlpatterns = [
    path("register/", views.register, name="register"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("change-password/", views.change_password, name="change_password"),
    path("change-contact/", views.change_contact, name="change_contact"),
]

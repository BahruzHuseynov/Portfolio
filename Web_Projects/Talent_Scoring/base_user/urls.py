from django.urls import path, reverse_lazy
from base_user import views
from django.contrib.auth import views as auth_views

app_name = "account"

urlpatterns = [
    path("register/", views.AccountRegistrationView.as_view(), name="register"),
    path("login/", views.AccountBaseLoginView.as_view(next_page=reverse_lazy("core:index")), name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page=reverse_lazy("core:index")),name="logout",),
]
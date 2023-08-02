from django.urls import path
from .views import *

urlpatterns = [
    path("not-accepted-url/", not_accepted_view, name="not_accepted"),
    path("need-approval-url/", not_approved_view, name="not_approved"),
    path("inactive-user/", inactive_user_view, name="inactive_user"),
    path("change-password/", change_password, name="change_password"),
    path("login/", login_view, name="login")
    path("dashboard/", dashboard_render,name="dashboard_url")
]

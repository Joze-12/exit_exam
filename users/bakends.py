# backends.py
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.shortcuts import redirect

User = get_user_model()

class CustomBackend(ModelBackend):
    def user_can_authenticate(self, user):
        return super().user_can_authenticate(user) and user.password_changed

    def authenticate(self, request, username=None, password=None, **kwargs):
        user = super().authenticate(request, username, password, **kwargs)
        if user and user.is_student() and user.studentprofile.rejected:
            return redirect("not_accepted_url")
        elif user and user.is_student() and not user.studentprofile.approved:
            return redirect('need_approval_url')  # Redirect to the "need_approval" page
        elif user and not user.is_active:
            return redirect('inactive_user_url')  # Redirect to the "inactive_user" page
        elif user and not user.password_changed:
            return redirect('change_password_url')  # Redirect to the change password page
        return user
    







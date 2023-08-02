from django.urls import path
from .views import *

urlpatterns = [
    path("create_question/", create_question_with_options, name="create_question_with_options")
]

from django.urls import path
from .views import *

urlpatterns = [
    path("create_question/", create_question_with_options, name="create_question_with_options"),
    path("list_question/", list_questions, name="questions_list"),
    path('start-practice/', start_practice, name='start_practice'),
    path('fetch-questions/', fetch_questions, name='fetch_questions'),
    path('practice-result/', practice_result, name='practice_result'),
]

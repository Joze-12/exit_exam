from django import forms
from django.forms import modelformset_factory
from .models import *

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ("question_text", "explanation")
        labels = {
            "question_text": "Question",
        }

OptionFormset = modelformset_factory(
    Options,
    fields=("value", ),
    labels= {
        "value": "Option"
    }
)
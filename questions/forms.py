from django import forms
from django.forms import modelformset_factory
from .models import *
from ckeditor.widgets import CKEditorWidget

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ("question_text", )
        labels = {
            "question_text": "Question",
        }
        widgets = {
            "question_text": CKEditorWidget()
        }

OptionFormset = modelformset_factory(
    Options,
    fields=("value", ),
    labels= {
        "value": "Option"
    }
)
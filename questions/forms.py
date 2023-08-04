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

class PracticeMenuForm(forms.ModelForm):
    number_of_questions = forms.IntegerField()
    class Meta:
        model = Question
        fields = ("number_of_questions", )

class ExamForm(forms.Form):
    def __init__(self, questions, *args, **kwargs):
        super(ExamForm, self).__init__(*args, **kwargs)
        for question in questions:
            choices = [(option.id, option.get_value()) for option in question.get_options()]
            self.fields[f'question_{question.id}'] = forms.ChoiceField(
                choices=choices,
                widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
            )
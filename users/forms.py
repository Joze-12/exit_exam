from django import forms
from .models import User, StudentProfile
from academics.models import Department
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Fieldset
from django.contrib.auth.forms import UserCreationForm



class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'mb-3 bg-light p-5'
        self.helper.layout = Layout(
            'username',
            'password',
            Submit('submit', 'Log In', css_class='btn-primary mt-3 w-100')
        )

class StudentSignupForm(UserCreationForm):
    student_id = forms.CharField(max_length=20, required=True)
    department = forms.ModelChoiceField(queryset=Department.objects.all())
    program = forms.ChoiceField(choices=StudentProfile.Program.choices)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('first_name', 'last_name', 'email') + UserCreationForm.Meta.fields + ('student_id', 'department', 'program')


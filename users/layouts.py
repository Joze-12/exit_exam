from crispy_forms.layout import Layout, Fieldset, Submit

class StudentSignUpFormLayout(Layout):
    def __init__(self):
        super().__init__(
            Fieldset('Personal Information',
                'first_name',
                'last_name',
                'username',
                'email',
                'password1',
                'password2',
            ),
            Fieldset('Student Information',
                'student_id',
                'program',
                'department',
            ),
            Submit('submit', 'Sign Up', css_class='btn btn-primary'),
        )

from django import forms

class AdminCreateUserForm(forms.Form):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=150)
    email = forms.EmailField()
    USER_TYPES = (
        ('Admin', "Admin"),
        ('Instructor', 'Instructor'),
        ('Student', 'Student'),
    )
    user_type = forms.ChoiceField(choices=USER_TYPES)

from django import forms

class AdminCreateUserForm(forms.Form):
    username = forms.CharField(max_length=150)
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=150)
    email = forms.EmailField()
    USER_TYPES = (
        ('Admin', "Admin"),
        ('Instructor', 'Instructor'),
        ('Student', 'Student'),
    )
    user_type = forms.ChoiceField(choices=USER_TYPES)
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirmation = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirmation = cleaned_data.get('password_confirmation')

        if password != password_confirmation:
            raise forms.ValidationError("Error: passwords do not match.")

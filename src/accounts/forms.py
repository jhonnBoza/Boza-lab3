from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    
    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "password1", "password2")
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['bio', 'birth_date', 'avatar']
        widgets = {
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'birth_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'avatar': forms.Select(choices=[
                ('👤', '👤 Default'),
                ('👨‍🎓', '👨‍🎓 Student'),
                ('👩‍🎓', '👩‍🎓 Student Female'),
                ('🧑‍💻', '🧑‍💻 Developer'),
                ('🎯', '🎯 Target'),
            ], attrs={'class': 'form-control'})
        }
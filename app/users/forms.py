from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from users.models import User, Skill


class CustomUserRegisterForm(UserCreationForm):
    role = forms.ChoiceField(choices=User.ROLE_CHOICES, required=True)
    birth_date = forms.DateField(
        widget=forms.TextInput(attrs={'type': 'date'}), required=False
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'role', 'phone', 'birth_date', 'password1',
                  'password2']


class UserProfileForm(UserChangeForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    username = forms.CharField(max_length=150)
    email = forms.EmailField()
    phone = forms.CharField(max_length=15, required=False)
    available = forms.BooleanField(required=False)
    skills = forms.ModelMultipleChoiceField(
        queryset=Skill.objects.all(),
        required=False
    )

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'username',
            'email',
            'phone',
            'available',
            'skills'
        )

from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from users.models import Skill, User


class CustomUserLoginForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Имя пользователя'}),
        label='Имя пользователя'
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Пароль'}),
        label='Пароль'
    )


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
    image = forms.ImageField(required=False)
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    username = forms.CharField(max_length=150)
    email = forms.EmailField()
    about_me = forms.Textarea()
    phone = forms.CharField(max_length=15, required=False)
    available = forms.BooleanField(required=False)
    skills = forms.ModelMultipleChoiceField(
        queryset=Skill.objects.all(),
        required=False
    )

    class Meta:
        model = User
        fields = ('image',
                  'first_name',
                  'last_name',
                  'username',
                  'email',
                  'about_me',
                  'phone',
                  'available',
                  'skills'
                  )

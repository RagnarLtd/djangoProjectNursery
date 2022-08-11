from django.contrib.auth import password_validation
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.validators import UnicodeUsernameValidator
from django import forms

from NurseryApp.models import Pet


class SingUpForm(UserCreationForm):
    username_validator = UnicodeUsernameValidator()
    username = forms.CharField(
        label='Username',
        max_length=150,
        help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.',
        validators=[username_validator],
        error_messages={'unique': "A user with that username already exists."},
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
        max_length=64,
        help_text='Введите адресс электронной почты'
    )
    shelter = forms.CharField(
        label='Shelter',
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        help_text='Введите название приюта'
    )
    address = forms.CharField(
        label='Address',
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        help_text='Введите адрес приюта'
    )
    password1 = forms.CharField(label='Password',
                                widget=(forms.PasswordInput(attrs={'class': 'form-control'})),
                                help_text=password_validation.password_validators_help_text_html())
    password2 = forms.CharField(label='Password Confirmation',
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}),
                                help_text='Повторно введите пароль')

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email', 'shelter', 'address',)


class CreatePetForm(forms.ModelForm):
    class Meta:
        model = Pet
        fields = ['nickname', 'age', 'weight', 'growth', 'special_signs']

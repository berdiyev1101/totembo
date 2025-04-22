from django.contrib.auth.forms import UserCreationForm
from django.forms import *

from totembo.models import CustomUser


class SignUpForm(UserCreationForm):
    password1 = CharField(widget=PasswordInput(attrs={
        "class":"form-control",
        "placeholder":"Password"
    }))
    password2 = CharField(widget=PasswordInput(attrs={
        "class": "form-control",
        "placeholder": "Re-Password"
    }))

    class Meta:
        model = CustomUser
        fields = ["email","first_name","country","phone_number"]
        widgets = {
             "email":EmailInput(attrs={
                "class": "form-control",
                "placeholder": "Email"
             }),
             "first_name":TextInput(attrs={
                "class": "form-control",
                "placeholder": "First Name"
             }),
            "phone_number":TextInput(attrs={
                "class": "form-control",
                "placeholder": "Phone Number"
            }),
            "country":TextInput(attrs={
                "class": "form-control",
                "placeholder": "Country"
            })
        }

class SignInForm(Form):
    email = EmailField(widget=EmailInput(attrs={
        "class":"form-control",
        "placeholder":"Email"
    }))
    password = CharField(widget=PasswordInput(attrs={
        "class": "form-control",
        "placeholder": "Password"
    }))

    class Meta:
        model = CustomUser
        fields = ["email", "password"]

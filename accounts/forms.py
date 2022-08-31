from dataclasses import fields
from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from accounts.models import User


class login_form(forms.Form):
    email = forms.EmailField( 
        label="ایمیل",
        )
    password = forms.CharField(
        label="رمز عبور",
        strip=False,
        widget=forms.PasswordInput,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None
        self.fields['email'].widget.attrs.update({'placeholder': 'ایمیل خود را وارد نمایید'})
        self.fields['password'].widget.attrs.update({'placeholder': 'رمز عبورتان را وارد نمایید'})

    def clean(self, *args, **kwargs):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")

        if email and password:
            self.user = authenticate(email=email, password=password)

            if self.user is None:
                raise forms.ValidationError("این کاربر وجود ندارد")
            if not self.user.check_password(password):
                raise forms.ValidationError("رمز عبورها مطابقت ندارند")
            if not self.user.is_active:
                raise forms.ValidationError("کاربر فعال نیست")

        return super(login_form, self).clean(*args, **kwargs)

    def get_user(self):
        return self.user

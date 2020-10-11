from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ('username', 'icon', 'age', 'email')


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('username', 'icon', 'age', 'email')


class CustomUserCreationModelForm(forms.ModelForm):

    class Meta:
        model = CustomUser
        fields = ('username', 'age', 'icon', 'email', 'password')
        widgets = {
            'password': forms.PasswordInput()
        }

    field_order = ['username', 'age', 'icon',
                   'email', 'email2', 'password', 'password2']

    password2 = forms.CharField(
        label='Password again',
        required=True,
        strip=False,
        widget=forms.PasswordInput()
    )

    email2 = forms.EmailField(
        label='Email address again',
        required=True,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'username-field'
        self.fields['age'].required = True
        self.fields['age'].widget.attrs['class'] = 'age-field'
        self.fields['email'].required = True
        self.fields['email'].widget.attrs['class'] = 'email-field'
        self.fields['email2'].required = True
        self.fields['email2'].widget.attrs['class'] = 'email-field'
        self.fields['password'].widget.attrs['class'] = 'password-field'
        self.fields['password2'].widget.attrs['class'] = 'password-field'

    def clean(self):
        super().clean()
        email = self.cleaned_data['email']
        email2 = self.cleaned_data['email2']

        if email != email2:
            raise forms.ValidationError(
                '"email address" and "email address again" are not match!'
            )

        password = self.cleaned_data['password']
        password2 = self.cleaned_data['password2']

        if password != password2:
            raise forms.ValidationError(
                '"password" and "password again" are not match!'
            )


class CustomUserChangeModelForm(forms.ModelForm):
    """パスワードは別の画面を用意して、そこで更新するようにする。"""

    class Meta:
        model = CustomUser
        fields = ('username', 'age', 'icon', 'email')
        # widgets = {
        #     'password': forms.PasswordInput()
        # }

    email2 = forms.EmailField(
        label='Email address again',
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['age'].required = True
        self.fields['email'].required = True
        self.fields['email2'].required = True

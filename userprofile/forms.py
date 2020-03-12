# 引入表单类
import copy

from django import forms
# 引入 User 模型
from django.contrib.auth.models import User
from django.contrib.auth import forms as auth_forms
from django.contrib.auth import authenticate


class UserLoginForm(forms.Form):
    username = forms.CharField(required=True, label_suffix='',
                               error_messages={'required': "username cannot be blank"},
                               widget=forms.TextInput(attrs={
                                   'label': 'Username',
                                   'class': 'form-control',
                                   'autofocus': '',

                               }))
    password = forms.CharField(required=True, label_suffix='',
                               error_messages={'required': "password cannot be blank"},
                               widget=forms.TextInput(attrs={
                                   'label': 'Password',
                                   'type': 'password',
                                   'class': 'form-control',
                               }))


class UserRegisterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        fields = self.base_fields

        for field_name in fields:
            field = fields[field_name]
            field.label_suffix = ''
            field.widget.attrs.update({'class': 'form-control'})
            # if field.errors:
            #     field.widget.attrs.update({'class': 'is-invalid'})

        super().__init__(*args, **kwargs)

    password = forms.CharField(required=True, label_suffix='', label='Password',
                               error_messages={'required': "password cannot be blank"},
                               widget=forms.TextInput(attrs={
                                   'type': 'password',
                                   'class': 'form-control',
                               }))
    password2 = copy.deepcopy(password)
    password2.label = 'Confirm Password'

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

        # widgets = {
        #     'email': forms.TextInput(attrs={'class': 'form-control',
        #                                     })
        # }

    def clean_password2(self):
        data = self.cleaned_data
        if data.get('password') == data.get('password2'):
            return data.get('password')
        else:
            raise forms.ValidationError("The password confirmation does not match.")

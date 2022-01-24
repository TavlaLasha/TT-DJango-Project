from django import forms
from django.contrib.auth import (authenticate, get_user_model)
from django.core.validators import validate_email

User = get_user_model()

class UserLoginForm(forms.Form):
    username = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Username', 'class': 'form-control', 'data-aos':'fade-up', 'data-aos-delay':'200'}))
    password = forms.CharField(label='', widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'form-control', 'data-aos':'fade-up', 'data-aos-delay':'200'}))

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError('This user does not exist')
            if not user.check_password(password):
                raise forms.ValidationError('Incorrect password')
            if not user.is_active:
                raise forms.ValidationError('This user is not active')
        
        return super(UserLoginForm, self).clean(*args, **kwargs)

class PasswordResetFrom(forms.Form):
    email = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'E-Mail', 'class': 'form-control', 'data-aos':'fade-up', 'data-aos-delay':'200'}))

    def clean(self, *args, **kwargs):
        email = self.cleaned_data.get('email')
        validate_email(email)
        if User.objects.filter(email=email).exists():
            user = User.objects.filter(email=email).get()
            if not user.is_active:
                raise forms.ValidationError('This user is not active')
        else:
            raise forms.ValidationError('This user does not exist')
        
        return super(PasswordResetFrom, self).clean(*args, **kwargs)


class UserRegisterForm(forms.ModelForm):
    error_class = 'error'
    email = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'E-Mail', 'class': 'form-control', 'data-aos':'fade-up', 'data-aos-delay':'200'}))
    username = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Username', 'class': 'form-control', 'data-aos':'fade-up', 'data-aos-delay':'200'}))
    firstname = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'First Name', 'class': 'form-control', 'data-aos':'fade-up', 'data-aos-delay':'200'}))
    lastname = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Last Name', 'class': 'form-control', 'data-aos':'fade-up', 'data-aos-delay':'200'}))
    password = forms.CharField(label='', widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'form-control', 'data-aos':'fade-up', 'data-aos-delay':'200'}))
    conf_password = forms.CharField(label='', widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password', 'class': 'form-control', 'data-aos':'fade-up', 'data-aos-delay':'200'}))
    phone = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Phone', 'class': 'form-control', 'data-aos':'fade-up', 'data-aos-delay':'200'}))
    agreesPolicy = forms.BooleanField(label='I agree with Terms & Policy')

    class Meta:
        model = User
        fields = [
            'email',
            'username',
            'firstname',
            'lastname',
            'password',
            'conf_password',
            'phone'
        ]

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        email = self.cleaned_data.get('email')
        firstname = self.cleaned_data.get('firstname')
        lastname = self.cleaned_data.get('lastname')
        phone = self.cleaned_data.get('phone')
        conf_password = self.cleaned_data.get('conf_password')
        agreesPolicy = self.cleaned_data.get('agreesPolicy')

        if not agreesPolicy:
            raise forms.ValidationError('You should agree with policy')

        if password != conf_password:
            raise forms.ValidationError('Passwords must match')
        
        validate_email(email)
        email_qs = User.objects.filter(email=email)
        if email_qs.exists():
            raise forms.ValidationError('This email is already being used')

        username_qs = User.objects.filter(username=username)
        if username_qs.exists():
            raise forms.ValidationError('This username is already being used')

        if not phone.isdecimal():
            raise forms.ValidationError('Phone should only contain numbers')

        if not (firstname.isalpha() and lastname.isalpha()):
            raise forms.ValidationError('Name should only contain letters')
            
        return super(UserRegisterForm, self).clean(*args, **kwargs)

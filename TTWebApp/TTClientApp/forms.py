from django import forms
from django.contrib.auth import (authenticate, get_user_model)
from django.core.validators import validate_email

from TTClientApp.models import Category, Cities, PaymentType, Product, Status, Supllier

User = get_user_model()
# For Products

categories = Category.objects.values_list('categoryid', 'categoryname')
suppliers = Supllier.objects.values_list('supllierid', 'companyname')
cities = Cities.objects.values_list('cityid', 'city')
status = Status.objects.values_list('statusid', 'status')
paymentTypes = PaymentType.objects.values_list('paymentid', 'payment')



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


class AddProductForm(forms.Form):
    name = forms.CharField(label='Product Name', max_length=80, required=True)
    categoryID = forms.ChoiceField(label='Category', choices=categories, required=True)
    # categoryID = forms.IntegerField(label='Category', required=True)
    picture = forms.FileField(label='Picture', required=True)
    price = forms.FloatField(label='Price', required=False)
    # supplierid = forms.IntegerField(label='Supplier', required=False)
    supplierid = forms.ChoiceField(label='Supplier', choices=suppliers, required=False)
    serialnumber = forms.CharField(label='Serial Number', max_length=50, required=False)
    description = forms.CharField(label='Description', required=False)

class AddOrderForm(forms.Form):
    cityid = forms.ChoiceField(label='City', choices=cities, required=True)
    shippostalcode = forms.CharField(label='Postal Code', required=True)
    address = forms.CharField(label='Address', required=True)
    statusid = forms.ChoiceField(label='Status', choices=status, required=True)
    paymenttype = forms.ChoiceField(label='Payment Type', choices=paymentTypes, required=True)
    statusdate = forms.CharField(label='Status date', required=True)
from django import forms
from django.contrib.auth import (authenticate, get_user_model)
from django.core.validators import validate_email
from .models import Category

from TTClientApp.models import Category, Product


class CategoryForm (forms.ModelForm):
    class Meta:
        model = Category
        fields = ['categoryname' ]

    
User = get_user_model()
# For Products
# CHOICES = [Category.objects.all()]
# # categories = Category.objects.all()
# # for i in categories:
# #     CHOICES.append(i.categoryid, i.categoryname)
# # print(CHOICES)




class UserLoginForm(forms.Form):
    username = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Username', 'class': ''}))
    password = forms.CharField(label='', widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': ''}))

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
    email = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'E-Mail', 'class': 'form-control'}))
    username = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Username', 'class': 'form-control'}))
    firstname = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'First Name', 'class': 'form-control'}))
    lastname = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Last Name', 'class': 'form-control'}))
    password = forms.CharField(label='', widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'form-control'}))
    conf_password = forms.CharField(label='', widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password', 'class': 'form-control'}))
    phone = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Phone', 'class': 'form-control'}))
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
    # categoryID = forms.ChoiceField(label='Category', choices=[CHOICES], required=True)
    categoryID = forms.IntegerField(label='Category', required=True)
    picture = forms.FileField(label='Picture', required=True)
    price = forms.FloatField(label='Price', required=False)
    supplierid = forms.IntegerField(label='Supplier', required=False)
    serialnumber = forms.CharField(label='Serial Number', max_length=50, required=False)
    description = forms.CharField(label='Description', required=False)

    # # productid = models.AutoField(db_column='ProductID', blank=True, primary_key=True)  # Field name made lowercase.
    # productname = models.CharField(db_column='ProductName', max_length=80)  # Field name made lowercase.
    # categoryid = models.ForeignKey(Category, db_column='CategoryID', on_delete=models.PROTECT, blank=True)  # Field name made lowercase.
    # picture = models.CharField(db_column='Picture', max_length=255)  # Field name made lowercase.
    # price = models.FloatField(db_column='Price', max_length=50, null=True)  # Field name made lowercase.
    # supllierid = models.ForeignKey(Supllier, db_column='SupllierID', on_delete=models.SET_NULL, blank=True, null=True)  # Field name made lowercase.
    # serialnumber = models.CharField(db_column='SerialNumber', max_length=50, null=True)  # Field name made lowercase.
    # discription = models.TextField(db_column='Discription', null=True)  # Field name made lowercase.

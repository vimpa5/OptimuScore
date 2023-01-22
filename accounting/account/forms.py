from django import forms
from .models import MyRegistration
from django.core.exceptions import NON_FIELD_ERRORS
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, SetPasswordForm
from django.core.exceptions import ValidationError

#Signup form

class MyRegistrationForm(UserCreationForm):
    password1=forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2=forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={'class':'form-control'}))
    class Meta:
        model=MyRegistration
        fields=['username', 'first_name', 'last_name', 'email', 'location', 'designation']
        widgets={
            'username':forms.TextInput(attrs={'class':'form-control'}),
            'first_name':forms.TextInput(attrs={'class':'form-control'}),
            'last_name':forms.TextInput(attrs={'class':'form-control'}),
            'email':forms.EmailInput(attrs={'class':'form-control'}),
            'location':forms.Select(attrs={'class':'form-select'}),
            'designation':forms.TextInput(attrs={'class':'form-control'}),
        }

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not username:
            raise ValidationError('Username is required!')
        else:
            try:
                MyRegistration.objects.get(username=username)
                raise ValidationError('This username already exists!', code='username_exists')
            except MyRegistration.DoesNotExist:
                pass
        return username

    def clean_email(self):
        email=self.cleaned_data.get('email')
        if not email:
            raise ValidationError('Email is required!')
        else:
            try:
                MyRegistration.objects.get(email=email)
                raise ValidationError('This email already exists!', code='email_exists')
            except MyRegistration.DoesNotExist:
                pass
        return email

    def clean_first_name(self):
        first_name=self.cleaned_data.get('first_name')
        if not first_name:
            raise ValidationError('First-name is required!')
        return first_name
    
    def clean_last_name(self):
        last_name=self.cleaned_data.get('last_name')
        if not last_name:
            raise ValidationError('Last-name is required!')
        return last_name
    
    def clean_location(self):
        location=self.cleaned_data.get('location')
        if not location:
            raise ValidationError('Location is required!')
        return location
    
    def clean_designation(self):
        designation=self.cleaned_data.get('designation')
        if not designation:
            raise ValidationError('Designation is required!')
        return designation

    # def clean(self):
    #     super().clean()
    #     if not self.instance.username:
    #         raise ValidationError('Username is required!')
    #     else:
    #         try:
    #             un=MyRegistration.objects.get(username=self.instance.username)
    #             raise ValidationError('This username already exists!')
    #         except MyRegistration.DoesNotExist:
    #             pass
    #     if not self.instance.email:
    #         raise ValidationError('email is required!')
    #     else:
    #         try:
    #             em=MyRegistration.objects.get(email=self.instance.email)
    #             raise ValidationError('This email already exists!')
    #         except MyRegistration.DoesNotExist:
    #             pass
    #     if not self.instance.first_name:
    #         raise ValidationError('first_name is required!')
    #     if not self.instance.last_name:
    #         raise ValidationError('last_name is required!')
    #     if not self.instance.location:
    #         raise ValidationError('location is required!')
    #     if not self.instance.designation:
    #         raise ValidationError('designation is required!')

#Login Form

class LoginForm(forms.Form):
    username=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'autofocus':True}))
    password=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))

# Password Change

class ChangePassword(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["new_password1"].widget = forms.PasswordInput(attrs={"class": "form-control"})
        self.fields["new_password2"].widget = forms.PasswordInput(attrs={"class": "form-control"})

#User Change Form Customisation

class ProfileForm(UserChangeForm):
    password=None
    class Meta:
        model=MyRegistration
        fields = ['username', 'first_name', 'last_name', 'email', 'location', 'designation', 'start_date', 'last_login']
        labels={'email': 'Email Address'}
        widgets={
            'username':forms.TextInput(attrs={'class':'form-control'}),
            'first_name':forms.TextInput(attrs={'class':'form-control'}),
            'last_name':forms.TextInput(attrs={'class':'form-control'}),
            'email':forms.EmailInput(attrs={'class':'form-control'}),
            'location':forms.Select(attrs={'class':'form-select'}),
            'designation':forms.TextInput(attrs={'class':'form-control'}),
            'start_date':forms.DateTimeInput(attrs={'class':'form-control'}),
            'last_login':forms.DateTimeInput(attrs={'class':'form-control'}),
        }

#Admin Change Form Customisation

class AdminProfileForm(UserChangeForm):
    password=None
    is_superuser=forms.BooleanField(label='Superuser', required=False, widget=forms.CheckboxInput(attrs={'class':'form-check-input'}))
    is_active=forms.BooleanField(label='Active', required=False, widget=forms.CheckboxInput(attrs={'class':'form-check-input'}))
    is_staff=forms.BooleanField(label='Staff', required=False, widget=forms.CheckboxInput(attrs={'class':'form-check-input'}))
    class Meta:
        model=MyRegistration
        fields = '__all__'
        labels={'email': 'Email Address'}
        # error_messages={
        #     NON_FIELD_ERRORS: {
        #         'username': "Username is required.",
        #     }
        # }
        widgets={
            # 'password':forms.PasswordInput(attrs={'class':'form-control'}),
            # 'groups':forms.ChoiceField(attrs={'class':'form-control'}),
            # 'user_permissions':forms.Select(attrs={'class':'form-control'}),
            'username':forms.TextInput(attrs={'class':'form-control'}),
            'email':forms.EmailInput(attrs={'class':'form-control'}),
            'first_name':forms.TextInput(attrs={'class':'form-control'}),
            'last_name':forms.TextInput(attrs={'class':'form-control'}),
            'location':forms.Select(attrs={'class':'form-select'}),
            'designation':forms.TextInput(attrs={'class':'form-control'}),
            'start_date':forms.DateTimeInput(attrs={'class':'form-control'}),
            'last_login':forms.DateTimeInput(attrs={'class':'form-control'}),
        }
from django import forms
from django_otp import forms as otp_forms
from accounts.forms import CustomUserCreationForm
from accounts.models import CustomUser
from .models import Manager, Trainee

class TraineeRegistrationForm(CustomUserCreationForm):
    phone = forms.CharField(max_length=100)
    address = forms.CharField(max_length=200)
    organization = forms.CharField(max_length=200)
    job = forms.CharField(max_length=100)
    
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'password1',
                   'password2', 'phone', 'address', 'organization', 'job')

class TraineeEditForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField(max_length=254)
    phone = forms.CharField(max_length=100)
    address = forms.CharField(max_length=200)
    job = forms.CharField(max_length=100)
    
    class Meta:
        model = Trainee
        fields = ('first_name', 'last_name', 'email', 'phone',
                  'address', 'job')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Exclude password field from form
        self.fields.pop('password1', None)
        self.fields.pop('password2', None)

class ManagerRegistrationForm(CustomUserCreationForm):
    phone = forms.CharField(max_length=100)
    organization = forms.CharField(max_length=200)
    
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'password1',
                   'password2', 'phone', 'organization')
        
class ManagerEditForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField(max_length=254)
    phone = forms.CharField(max_length=100)
    organization = forms.CharField(max_length=100)
    
    class Meta:
        model = Manager
        fields = ('first_name', 'last_name', 'email', 'phone', 'organization')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Exclude password field from form
        self.fields.pop('password1', None)
        self.fields.pop('password2', None)

        
class AuthenticationTokenForm(forms.Form):
    token = forms.CharField(
        label='OTP',
        help_text='Enter the six-digit code from your Google Authenticator app.',
        widget=forms.TextInput(attrs={'autocomplete': 'off'})
    )
        

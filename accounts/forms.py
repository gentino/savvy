from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
from phonenumber_field.formfields import PhoneNumberField

def styles():
    return '''w-full pl-12 pr-4 py-3
    bg-surface-container-low
    border border-outline-variant rounded-xl
    focus:ring-2 focus:ring-primary
    focus:border-transparent
    transition-all
    outline-none
    font-body-md
    text-on-surface
    '''

class RegisterForm(UserCreationForm):
    phone = PhoneNumberField(
        region="NG",
        widget=forms.TextInput(attrs={
            "placeholder": "Phone Number",
            "type": "tel",
        })
    )
    class Meta:
        model = User
        fields = (
            "profile_photo",
            "first_name",
            "last_name",
            "username",
            "email",
            "phone",
            "password1",
            "password2",
        )

        widgets = {
            "first_name": forms.TextInput(attrs={
                "placeholder": "First Name"
            }),
            "last_name": forms.TextInput(attrs={
                "placeholder": "Last Name"
            }),
            "username": forms.TextInput(attrs={
                "placeholder": "Username"
            }),
            "email": forms.EmailInput(attrs={
                "placeholder": "Email Address"
            }),
            # "phone": forms.TextInput(attrs={
            #     "placeholder": "Phone Number"
            # }),
            
            
            
            'profile_photo': forms.ClearableFileInput(
                attrs={
            "class": "hidden",
            "accept": "image/*"
            })   
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
      
        for name, field in self.fields.items():
            if name == "profile_photo":
                continue
            field.widget.attrs["class"] = styles()
        

class LoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class':styles(),
            "placeholder": "Email Address"
        })
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class':styles(),
            "placeholder": "••••••••",
            'id':"password"
        })
    )

    remember_me = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={
        'class':'w-4 h-4 text-primary bg-surface-container border-outline-variant rounded focus:ring-primary',
    }
    )
    )
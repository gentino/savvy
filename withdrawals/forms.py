from django import forms
from .models import BankInfo,Withdrawal

def styles():
    return '''
    w-full px-sm py-sm rounded-xl border 
    border-outline-variant bg-surface-container-lowest focus:ring-2 
    focus:ring-primary focus:border-primary transition-all text-on-surface 
    placeholder:text-on-surface-variant/50'''

class BankForm(forms.ModelForm):

    
    
    class Meta:
        fields = ['bank_name','account_number','account_name']
        model =BankInfo
        
        widgets ={
            'bank_name':forms.TextInput(attrs={
                'class':styles(),
                'placeholder': 'Access Bank',
                'required':True
            }),
            'account_number':forms.TextInput(attrs={
                "placeholder": "Account Number",
                "inputmode": "numeric",
                "autocomplete": "off",
                "maxlength": "10",
                "pattern": "[0-9]{10}",
                'required':True,
                'class':styles(),
                
            }),
            'account_name':forms.TextInput(attrs={
                'class':styles(),
                'placeholder': 'Access Bank',
                'required':True,
                'class':styles(),
            })
        }
        
    def clean_account_number(self):
        account_number = self.cleaned_data["account_number"]

        if not account_number.isdigit():
            raise forms.ValidationError(
                "Account number must contain only numbers."
            )

        if len(account_number) != 10:
            raise forms.ValidationError(
                "Account number must be 10 digits."
            )

        return account_number

class WithdrawalForm(forms.ModelForm):
    class Meta:
        fields = ['amount']
        model = Withdrawal
        
        
        widgets={
            'amount':forms.TextInput(attrs={
            "placeholder": "Enter amount",
            "inputmode": "decimal",
            "autocomplete": "off",
            "min": "1",
            "step": "0.01",
            "required": True,
            "class": styles(),
                
            })
        }
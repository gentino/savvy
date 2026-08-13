from django import forms
from .models import Deposit


def styles():
    return """
    w-full pl-10 py-sm rounded-xl border 
    border-outline-variant bg-surface-container-lowest focus:ring-2 
    focus:ring-primary focus:border-primary transition-all text-on-surface 
    placeholder:text-on-surface-variant/50"""


class DepositForm(forms.ModelForm):

    class Meta:
        model = Deposit
        fields = ["amount"]

        widgets = {
            "amount": forms.NumberInput(
                attrs={
                    "placeholder": "Enter amount",
                    "inputmode": "decimal",
                    "autocomplete": "off",
                    "min": "100",
                    "step": "0.01",
                    "required": True,
                    "class": styles(),
                }
            )
        }

    def clean_amount(self):
        amount = self.cleaned_data.get("amount")

        if amount is None:
            raise forms.ValidationError("Please enter a deposit amount.")

        if amount < 100:
            raise forms.ValidationError("Minimum deposit amount is ₦100.")

        return amount

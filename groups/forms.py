from django import forms
from .models import Group

class GroupForm(forms.ModelForm):
    class Meta:
        fields=['name','description', 'group_image', 'contribution_amount','contribution_frequency','max_members', 'duration','is_active']
        model =Group

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full rounded-lg border border-gray-300 px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500',
                'id': 'name',
                'placeholder': 'Enter group name',
            }),

            'description': forms.Textarea(attrs={
                'class': 'w-full rounded-lg border border-gray-300 px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500',
                'id': 'description',
                'rows': 4,
                'placeholder': 'Describe your group',
            }),

            'group_image': forms.ClearableFileInput(attrs={
                'class': 'hidden',
                'id': 'image',
                'accept': 'image/*',
            }),

            'contribution_amount': forms.NumberInput(attrs={
                'class': 'w-full rounded-lg border border-gray-300 px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500',
                'id': 'contribution_amount',
                'placeholder': '0.00',
                'min': '1',
            }),

            'contribution_frequency': forms.Select(attrs={
                'class': 'w-full rounded-lg border border-gray-300 px-4 py-2 bg-white focus:outline-none focus:ring-2 focus:ring-blue-500',
                'id': 'contribution_frequency',
            }),

            'duration': forms.NumberInput(attrs={
                    'class': 'w-full rounded-lg border border-gray-300 px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500',
                    'id': 'max_members',
                    'min': '2',
                    
                }),

            'max_members': forms.NumberInput(attrs={
                'class': 'w-full rounded-lg border border-gray-300 px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500',
                'id': 'max_members',
                'min': '2',
                'placeholder': '20',
            }),

            'is_active': forms.CheckboxInput(attrs={
                'class': 'h-5 w-5 text-blue-600 rounded focus:ring-blue-500',
                'id': 'is_active',
            }),
        }
        
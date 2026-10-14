from django import forms
from django.contrib.auth.models import User
from .models import Profile, Supplier, Purchase


class RegisterForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput,
        label='Confirm Password'
    )

    class Meta:
        model = User
        fields = ['username', 'email']

    def clean(self):
        cleaned_data = super().clean()

        if cleaned_data.get('password') != cleaned_data.get(
            'confirm_password'
        ):
            raise forms.ValidationError(
                'Passwords do not match.'
            )

        return cleaned_data


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['full_name', 'phone', 'address', 'picture']


class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ['supplier_name', 'contact_number', 'address']


class PurchaseForm(forms.ModelForm):
    class Meta:
        model = Purchase
        fields = [
            'supplier',
            'product_name',
            'quantity',
            'unit_price',
            'discount',
            'paid_amount',
            'purchase_date',
        ]
        widgets = {
            'purchase_date': forms.DateInput(
                attrs={'type': 'date'}
            ),
        }
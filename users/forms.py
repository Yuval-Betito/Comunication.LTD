from django import forms
from .models import Customer
from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from .models import User


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'customer_id', 'phone_number', 'email']

    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        if "'" in first_name or '"' in first_name:
            raise forms.ValidationError("Invalid character in first name.")
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data['last_name']
        if "'" in last_name or '"' in last_name:
            raise forms.ValidationError("Invalid character in last name.")
        return last_name

    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        if not phone_number.startswith('05'):
            raise forms.ValidationError("Phone number must start with '05'.")
        if len(phone_number) != 10:
            raise forms.ValidationError("Phone number must be exactly 10 digits long.")
        return phone_number

    def clean_email(self):
        email = self.cleaned_data.get('email')


        from django.core.validators import validate_email
        from django.core.exceptions import ValidationError

        try:
            validate_email(email)
        except ValidationError:
            raise forms.ValidationError("Invalid email format. Please enter a valid email address.")


        if Customer.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already associated with another customer.")

        return email




class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'placeholder': 'Enter your email'}),
        label="Email"
    )

    def clean_email(self):
        email = self.cleaned_data.get('email')


        try:
            validate_email(email)
        except ValidationError:
            raise forms.ValidationError("Invalid email format. Please enter a valid email address.")


        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError("If this email exists in our system, you will receive an email with further instructions.")

        return email



class ResetPasswordForm(forms.Form):
        token = forms.CharField(widget=forms.HiddenInput())
        new_password = forms.CharField(widget=forms.PasswordInput(), label="New Password")
        confirm_password = forms.CharField(widget=forms.PasswordInput(), label="Confirm Password")

        def clean(self):
            cleaned_data = super().clean()
            new_password = cleaned_data.get("new_password")
            confirm_password = cleaned_data.get("confirm_password")

            if new_password != confirm_password:
                raise forms.ValidationError("Passwords do not match.")
            return cleaned_data
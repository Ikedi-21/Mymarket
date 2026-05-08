from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User, SellerProfile

class RegistrationForm(UserCreationForm):
    role = forms.ChoiceField(choices=User.ROLE_CHOICES, required=True)
    display_name = forms.CharField(max_length=255, required=False, help_text="Required for sellers")
    bio = forms.CharField(required=False, widget=forms.Textarea, help_text="Required for sellers")

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email', 'role')

    def clean(self):
        cleaned_data = super().clean()
        role = cleaned_data.get('role')
        display_name = cleaned_data.get('display_name')
        bio = cleaned_data.get('bio')

        if role == 'seller':
            if not display_name:
                self.add_error('display_name', 'Sellers must have a display name.')
            if not bio:
                self.add_error('bio', 'Sellers must have a bio.')
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=commit)
        user.role = self.cleaned_data['role']
        if commit:
            user.save()
            if user.role == 'seller':
                SellerProfile.objects.create(
                    user=user,
                    display_name=self.cleaned_data['display_name'],
                    bio=self.cleaned_data['bio']
                )
        return user

class LoginForm(AuthenticationForm):
    pass

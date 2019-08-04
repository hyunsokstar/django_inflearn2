from django.contrib.auth.forms import UserCreationForm
from .models import Profile
from django import forms

class SignupForm(UserCreationForm):
    phone = forms.CharField()
    address = forms.CharField()

    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields

    def save(self):
        user = super().save()
        profile = Profile.objects.create(
            user = user,
            phone = self.cleaned_data['phone'],
            address = self.cleaned_data['address']
		)
        return user

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


from django.contrib.auth.forms import AuthenticationForm
from django import forms

class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Username", max_length=30,
        widget=forms.TextInput(attrs={'class': 'mdl-textfield__input', 'type' :'text', 'id' : 'username'}))
    password = forms.CharField(label="Password", max_length=30,
        widget=forms.TextInput(attrs={'class': 'mdl-textfield__input', 'type' :'password', 'id' : 'password'}))

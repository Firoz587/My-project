from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
class SignUpForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'id':'required'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'id':'required'}))
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        
class UpdateUserData(UserChangeForm):
    password = None
    first_name = forms.CharField(widget=forms.TextInput(attrs={'id':'required'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'id':'required'}))
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        
from django.shortcuts import render, redirect
from django.contrib.auth.forms import PasswordChangeForm, SetPasswordForm
from django.contrib.auth import update_session_auth_hash, logout
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from . import forms
from car.models import Purchase
# Create your views here.
def signup(request):
    if request.method == 'POST':
        signup_form = forms.SignUpForm(request.POST)
        if signup_form.is_valid():
            signup_form.save()
            messages.success(request, 'Account Created Successfully!')
            return redirect ('login')
    else:
        signup_form = forms.SignUpForm(request.POST)
        
    return render(request, 'authentication.html', {'form': signup_form, 'heading': 'Create New Account', 'btn_text': 'Create'})
class UserLoginView(LoginView):
    template_name = 'authentication.html'
    def get_success_url(self): 
        return reverse_lazy('profile')
    
    def form_valid(self, form):
        messages.success(self.request, 'Logged in Successfully!')
        return super().form_valid(form)
    def form_invalid(self, form):
        messages.warning(self.request, 'Login information is incorrect!')
        return super().form_invalid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['heading'] = 'Login to Your Account'
        context['btn_text'] = 'Login'
        return context    
@login_required 
def profile(request):
    orders = Purchase.objects.filter(user=request.user).order_by('-purchased_on')
    return render(request, 'profile.html', {'orders': orders})
@login_required    
def update_profile(request):
    if request.method == 'POST':
        profile_form = forms.UpdateUserData(request.POST, instance=request.user)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'Profile Updated Successfully!')
            return redirect('profile')
    else:
        profile_form = forms.UpdateUserData(instance=request.user)
        
    return render(request, 'update_profile.html', {'form': profile_form})
@login_required
def change_password(request):
    if request.method == 'POST':
        change_pass_form = PasswordChangeForm(request.user, data=request.POST)
        if change_pass_form.is_valid():
            change_pass_form.save()
            messages.success(request, 'Password Updated Successfully!')
            update_session_auth_hash(request, change_pass_form.user)
            return redirect('profile')
    else:
        change_pass_form = PasswordChangeForm(user=request.user)
        
    return render(request, 'change_password.html', {'form': change_pass_form})
@login_required
def reset_password(request):
    if request.method == 'POST':
        reset_pass_form = SetPasswordForm(user=request.user, data=request.POST)
        if reset_pass_form.is_valid():
            reset_pass_form.save()
            messages.success(request, 'Password Reset Successfully!')
            update_session_auth_hash(request, reset_pass_form.user)
            return redirect('profile')
    else:
        reset_pass_form = SetPasswordForm(user=request.user)
    return render(request, 'reset_password.html', {'form': reset_pass_form})
@login_required 
def user_logout(request):
    logout(request)
    messages.success(request, 'Logged Out Successfully!')
    return redirect('login')
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib import messages
from .forms import BrandForm
from .models import Brand
@method_decorator(login_required, name='dispatch')
class AddBrandView(CreateView):
    model = Brand
    form_class = BrandForm
    template_name = 'add_brand.html'
    success_url = reverse_lazy('add_brand')    
    
    def form_valid(self, form):
        messages.success(self.request, 'Brand Added Successfully!')
        return super().form_valid(form)
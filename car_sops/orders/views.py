from django.views import View
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Order
from posts.models import Post
from . import models
class BuyCarView(LoginRequiredMixin, View):
    def post(self, request, pk):
        car = models.Post.objects.get(pk=pk) 
        if car.quantity > 0:
            Order.objects.create(user=request.user, car=car)
            car.quantity -= 1
            car.save()
        return redirect('profile')
    
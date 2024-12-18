from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib import messages
from .forms import CarForm, CommentForm
from .models import Car, Purchase
# Create your views here.
class CarDetailsView(DetailView):
    model = Car
    pk_url_kwarg = 'id'
    template_name = 'view_car.html'
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        comment_form = CommentForm(data=request.POST)
        
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.car = self.object
            new_comment.save()
            return redirect('view_car', id=self.object.pk)
        
        return self.get(request, *args, **kwargs)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        car = self.object
        comments = car.comments.all().order_by('-id')        
        comment_form = CommentForm()
        context['comments'] = comments
        context['comment_form'] = comment_form
        return context
@method_decorator(login_required, name='dispatch')
class AddCarView(CreateView):
    model = Car
    form_class = CarForm
    template_name = 'add_car.html'
    success_url = reverse_lazy('home')
    
    def form_valid(self, form):
        messages.success(self.request, 'Car Added Successfully!')
        return super().form_valid(form)
@method_decorator(login_required, name='dispatch')
class EditCarView(UpdateView):
    model = Car
    form_class = CarForm
    template_name = 'edit_car.html'
    pk_url_kwarg = 'id'
    success_url = reverse_lazy('home')
    
@method_decorator(login_required, name='dispatch')
class DeleteCarView(DeleteView):
    model = Car
    template_name = 'delete_car.html'
    pk_url_kwarg = 'id'
    success_url = reverse_lazy('home')
    
@login_required
def BuyCarView(request, id):
    car = Car.objects.get(pk=id)
    if car.quantity > 0:
        car.quantity -= 1
        car.save()
        Purchase.objects.create(user=request.user, car=car, quantity=1)
        return render(request, 'buy_car.html', {'car': car, 'tag': 'success', 'msg': 'You successfully bought this car!'})
    else:
        return render(request, 'buy_car.html', {'car': car, 'tag': 'danger', 'msg': 'Oops! This Car stock is out!'})
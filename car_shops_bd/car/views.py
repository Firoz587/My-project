from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib import messages
from .forms import CarForm, CommentForm
from .models import Car, Purchase
from sslcommerz_lib import SSLCOMMERZ 
from car.models import Purchase,Car
import random,string
from django.views.decorators.csrf import csrf_exempt
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

def unique_transactions_id_generator(size=10,chars=string.ascii_uppercase+string.digits):
    return ''.join(random.choice(chars)for _ in range(size))

# @login_required
# def BuyCarView(request, id):
#     car = Car.objects.get(pk=id)
#     if car.quantity > 0:
#         car.quantity -= 1
#         car.save()
#         Purchase.objects.create(user=request.user, car=car, quantity=1)
#         order_qs = Purchase.objects.filter(user=request.user).first()
#         settings = { 'store_id': 'bdjew67b71659ea172', 'store_pass': 'bdjew67b71659ea172@ssl', 'issandbox': True }
#         sslcz = SSLCOMMERZ(settings)
#         post_body = {}
#         post_body['total_amount'] = order_qs
#         post_body['currency'] = "BDT"
#         post_body['tran_id'] = unique_transactions_id_generator()
#         post_body['success_url'] = "http://127.0.0.1:8000/user/profile/"
#         post_body['fail_url'] = "http://127.0.0.1:8000/"
#         post_body['cancel_url'] = "http://127.0.0.1:8000/"
#         post_body['emi_option'] = 0
#         post_body['cus_name'] = request.user.username
#         post_body['cus_email'] = request.user.email
#         post_body['cus_phone'] = "01700000000"
#         post_body['cus_add1'] = "Uttara"
#         post_body['cus_city'] = "Dhaka"
#         post_body['cus_country'] = "Bangladesh"
#         post_body['shipping_method'] = "NO"
#         post_body['multi_card_name'] = ""
#         post_body['num_of_item'] = 1
#         post_body['product_name'] = "Test"
#         post_body['product_category'] = "Test Category"
#         post_body['product_profile'] = "general"


#         response = sslcz.createSession(post_body) 
#         print(response)
#         return redirect(response['GatewayPageURL'])
#         # return render(request, 'buy_car.html', {'car': car, 'tag': 'success', 'msg': 'You successfully bought this car!'})
#     else:
#         return render(request, 'buy_car.html', {'car': car, 'tag': 'danger', 'msg': 'Oops! This Car stock is out!'})
@login_required
def BuyCarView(request, id):
    car = get_object_or_404(Car, pk=id)

    if car.quantity > 0:
        car.quantity -= 1
        car.save()
        purchase = Purchase.objects.create(user=request.user, car=car, quantity=1)

        # SSLCommerz Configuration
        settings = {
            'store_id': 'bdjew67b71659ea172',
            'store_pass': 'bdjew67b71659ea172@ssl',
            'issandbox': True
        }
        sslcz = SSLCOMMERZ(settings)

        post_body = {
            'total_amount': str(car.price),  # Ensure price is passed as a string
            'currency': "BDT",
            'tran_id': unique_transactions_id_generator(),
            'success_url': "http://127.0.0.1:8000/user/profile/",
            'fail_url': "http://127.0.0.1:8000/",
            'cancel_url': "http://127.0.0.1:8000/",
            'emi_option': 0,
            'cus_name': request.user.username,
            'cus_email': request.user.email,
            'cus_phone': "01700000000",
            'cus_add1': "Uttara",
            'cus_city': "Dhaka",
            'cus_country': "Bangladesh",
            'shipping_method': "NO",
            'multi_card_name': "",
            'num_of_item': 1,
            'product_name': car.title,
            'product_category': "Car",
            'product_profile': "general"
        }

        response = sslcz.createSession(post_body)

        if 'GatewayPageURL' in response:
            return redirect(response['GatewayPageURL'])
        else:
            return render(request, 'buy_car.html', {'car': car, 'tag': 'danger', 'msg': 'Payment gateway error!'})

    else:
        return render(request, 'buy_car.html', {'car': car, 'tag': 'danger', 'msg': 'Oops! This Car stock is out!'})
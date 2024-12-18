from django.urls import path
from .views import BuyCarView

urlpatterns = [
    path('buy/<int:pk>/', BuyCarView.as_view(), name='buy_car'),
]

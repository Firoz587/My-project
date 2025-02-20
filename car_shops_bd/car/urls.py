from django.urls import path
from .views import CarDetailsView, AddCarView, EditCarView, DeleteCarView, BuyCarView
from . import views
urlpatterns = [    
    path('view/<int:id>/', CarDetailsView.as_view(), name='view_car'),
    path('add/', AddCarView.as_view(), name='add_car'),
    path('edit/<int:id>', EditCarView.as_view(), name='edit_car'),
    path('delete/<int:id>', DeleteCarView.as_view(), name='delete_car'),
    path('buy_now/<int:id>/', BuyCarView, name='buy_now'),
    # path('pay/', views.payment, name='payment'),
]
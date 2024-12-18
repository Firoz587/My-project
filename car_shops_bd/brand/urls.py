from django.urls import path
from .views import AddBrandView
urlpatterns = [    
    path('add/', AddBrandView.as_view(), name='add_brand'),
]
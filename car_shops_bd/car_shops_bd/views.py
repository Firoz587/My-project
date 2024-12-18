from django.shortcuts import render
from car.models import Car
from brand.models import Brand
# Create your views here.
def home(request, brand_slug=None):
    brands = Brand.objects.all().order_by('name')
    if brand_slug is not None:
        brand = Brand.objects.get(slug=brand_slug)
        cars = Car.objects.filter(brand=brand).order_by('title')
    else:
        cars = Car.objects.all().order_by('title')
    return render(request, 'home.html', {'cars': cars, 'brands': brands})
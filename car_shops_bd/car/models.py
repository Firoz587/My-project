from django.db import models
from django.contrib.auth.models import User
from brand.models import Brand
# Create your models here.
class Car(models.Model):
    image = models.ImageField(upload_to='car/media/uploads/', blank=True, null=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE) 
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
    
class Purchase(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    quantity = models.PositiveIntegerField()
    purchased_on = models.DateTimeField(auto_now_add=True)

    
    def __str__(self):
        return f"{self.user.username} bought {self.quantity} of {self.car.title}"
    
class Comment(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=100)
    comment = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Comment by {self.name}"
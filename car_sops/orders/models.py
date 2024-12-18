from django.db import models
from django.contrib.auth.models import User
from posts.models import Post

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    car = models.ForeignKey(Post, on_delete=models.CASCADE)
    purchased_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} bought {self.car.name}"

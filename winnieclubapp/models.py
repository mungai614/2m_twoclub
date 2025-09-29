from django.db import models
from django.contrib.auth.models import User



class Member(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Link to Django's built-in User
    phone = models.CharField(max_length=15, blank=True)
    joined_date = models.DateField(auto_now_add=True)
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.user.username


class Event(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    event_date = models.DateTimeField()
    created_by = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True)
    location = models.CharField(max_length=200)

    def __str__(self):
        return self.title


class StockItem(models.Model):
    name = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name


class Worker(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=200)
    photo = models.ImageField(upload_to='worker_photos/')

    def __str__(self):
        return self.name

from django.db import models
from django.contrib.auth.models import User
from datetime import date

class Member(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
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
    name = models.CharField(max_length=200)
    quantity = models.PositiveIntegerField()
    buying_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    min_stock_level = models.PositiveIntegerField(default=5)

    def __str__(self):
        return self.name

class Worker(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=200)
    photo = models.ImageField(upload_to='worker_photos/')

    def __str__(self):
        return self.name

class Sale(models.Model):
    stock_item = models.ForeignKey(StockItem, on_delete=models.CASCADE)
    buying_price = models.DecimalField(max_digits=10, decimal_places=2)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    date_sold = models.DateField(default=date.today)
    quantity_sold = models.PositiveIntegerField()

    @property
    def profit(self):
        return (self.selling_price - self.buying_price) * self.quantity_sold

    def __str__(self):
        return f"Sale of {self.stock_item.name} on {self.date_sold}"

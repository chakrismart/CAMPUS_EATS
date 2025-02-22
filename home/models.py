from django.db import models
from django.utils.timezone import now
from django.utils import timezone
# Create your models here.
import datetime

import pytz

class Category(models.Model):
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name
    

class Customer(models.Model):
    username = models.CharField(max_length=50, unique=True)  # Make username unique
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=10)
    email = models.EmailField(max_length=100, unique=True)
    
    branch = models.CharField(max_length=50, blank=True, null=True)  # Added branch
    registered_no = models.CharField(max_length=10, blank=True, null=True)  # Added regno
    profile_updated = models.BooleanField(default=False)
    old_cart=models.CharField(max_length=100,blank=True,null=True)

    def __str__(self):
        return self.username




class Product(models.Model):
    name=models.CharField(max_length=100)
    price=models.DecimalField(default=0,decimal_places=2,max_digits=6)
    category=models.ForeignKey(Category,on_delete=models.CASCADE,default=1)
    is_available=models.BooleanField(default=True)
    image=models.ImageField(upload_to='pics')
    
    def __str__(self):
        return self.name

# Create your models here.



class Orders(models.Model):
    order_id = models.CharField(max_length=20, unique=True, blank=True)
    transaction_id = models.CharField(max_length=50, blank=True, null=True)
    customer_name = models.CharField(max_length=100, blank=True)
    items = models.JSONField()  # Stores product IDs and quantities
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, default="Pending")  # "Pending" or "Paid"
    created_at = models.DateField()  # Store only the date (no time)

    def save(self, *args, **kwargs):
        # Convert to IST before saving and store only date part
        india_tz = pytz.timezone('Asia/Kolkata')
        if not self.created_at:
            now = timezone.now().astimezone(india_tz)  # Get current datetime in IST
            self.created_at = now.date()  # Store only the date part
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order {self.order_id} - {self.status}"

from django.contrib import admin
from .models import Product,Category,Orders,Customer
# Register your models here.
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Orders)
admin.site.register(Customer)



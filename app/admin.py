from django.contrib import admin
from .models import Contact,ProductItems,MyOrders,Medicines
# Register your models here.
admin.site.register(Contact)
admin.site.register(Medicines)
admin.site.register(ProductItems)
admin.site.register(MyOrders)
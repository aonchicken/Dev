from django.contrib import admin
from .models import Product,Customer,Staff,Document,Goods,Question,Choice
# Register your models here.

admin.site.register(Product)
admin.site.register(Customer)
admin.site.register(Staff)
admin.site.register(Document)
admin.site.register(Goods)
admin.site.register(Question)
admin.site.register(Choice)

from django.contrib import admin
from .models import (
    BotUser,
    Category,
    Product,
    ShopCard,
    Order,
    OrderCredit
)


# Register your models here.

@admin.register(BotUser)
class BotUserAdmin(admin.ModelAdmin):
    list_display = ['id', 'full_name', 'user_id', 'contact']
    search_fields = ['user_id', 'full_name']
    exclude = ['number', 'number1', 'month', 'protsent', 'language', 'bot_state']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'parent']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    search_fields = ['naem']
    list_display = ['id', 'title', 'category', 'price']


@admin.register(ShopCard)
class ShopCardAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'product', ]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    search_fields = ['status','check']
    list_display = ['id', 'user', 'products', 'count', 'all_price', 'status', 'check']


@admin.register(OrderCredit)
class OrderCreditAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'products', 'all_price']

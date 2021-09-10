from django.contrib import admin
from .models import ShoppingCart, ProductsInCart

admin.site.register(ShoppingCart)
admin.site.register(ProductsInCart)

from django.contrib import admin
from .models import BuyOrder, ItemsInOrder

admin.site.register(BuyOrder)
admin.site.register(ItemsInOrder)

import uuid
from django.db import models
from django.core.validators import MinValueValidator

from applications.products.models import Product


class BuyOrder(models.Model):
    """This model is generated only when the shopping cart contains only
    valid item based on the minimum value"""

    id = models.UUIDField(primary_key=True,
                          default=uuid.uuid4,
                          editable=False)

    total_price = models.DecimalField(max_digits=20, decimal_places=2)

    def items(self):
        return [{
            'id': x.product.id,
            'name': x.product.name,
            'price': float(x.product.price),
            'minimum': x.product.minimum,
            'amount-per-package': x.product.max_availability,
            'quantity': x.quantity,
            } for x in self.items_in_order.all()]

    def __str__(self):
        return f'Buy Order: {self.id}'


class ItemsInOrder(models.Model):
    """This model will get all the order items into it"""

    order = models.ForeignKey(
        BuyOrder,
        on_delete=models.CASCADE,
        related_name='items_in_order')

    product = models.ForeignKey(
        Product, on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])

    def __str__(self):
        return f'Item {self.id}'

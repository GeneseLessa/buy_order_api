from django.db import models
from django.core.validators import MinValueValidator

from applications.products.models import Product


class ShoppingCart(models.Model):
    """The Shopping Cart is the base for product adding and the order is
    generated from checkout of cart"""

    is_active = models.BooleanField(default=True)

    def products_validated(self):
        for i in self.items_in_cart.all():
            if not i.quantity_validate():
                return False

        return True

    def products_clean(self):
        """Remove all cart products"""
        for i in self.items_in_cart.all():
            i.delete()

    def total_value(self):
        total = 0
        for i in self.items_in_cart.all():
            total += i.value()
        return total

    def __str__(self):
        return f'Cart: {self.id}'


class ProductsInCart(models.Model):
    """This model is responsible for host products related to some cart and
    this is a base for order creation"""

    cart = models.ForeignKey(
        ShoppingCart,
        on_delete=models.CASCADE,
        related_name='items_in_cart')

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='products_in_cart')

    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    is_active = models.BooleanField(default=True)

    def quantity_validate(self):
        has_minimum = self.quantity >= self.product.minimum
        is_package_multiple = self.quantity % self.product.amount_per_package

        return has_minimum and not is_package_multiple

    def value(self):
        return self.quantity * self.product.price

    def __str__(self):
        return f'{self.product}: {self.quantity}'

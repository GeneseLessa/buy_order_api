from django.db import models
from django.core.validators import MinValueValidator


class Product(models.Model):
    """This class is responsible for modeling the ORM Product model.
    The fields are:

    name, price, minimum, amount_per_package, max_availability"""

    name = models.CharField(max_length=150, unique=True)

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)])

    minimum = models.PositiveIntegerField(validators=[MinValueValidator(0)])

    amount_per_package = models.PositiveIntegerField(
        validators=[MinValueValidator(0)])

    max_availability = models.PositiveIntegerField(
        validators=[MinValueValidator(0)])

    def __str__(self):
        return self.name

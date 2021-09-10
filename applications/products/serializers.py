from rest_framework import serializers
from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    """This class is responsible for serialization and desserialization of
    products"""

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'price', 'minimum',
            'amount-per-package', 'max-availability'
        ]
        extra_kwargs = {
            'amount-per-package': {'source': 'amount_per_package'},
            'max-availability': {'source': 'max_availability'}
        }

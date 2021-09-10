from rest_framework import serializers
from .models import ShoppingCart, ProductsInCart


class ShoppingCartSerializer(serializers.ModelSerializer):
    # total_value = serializers.DecimalField(max_digits=20, decimal_places=2)

    class Meta:
        model = ShoppingCart
        fields = '__all__'


class ShoppingCartItemsSerializer(serializers.ModelSerializer):
    items_in_cart = serializers.StringRelatedField(many=True)

    class Meta:
        model = ShoppingCart
        fields = ['items_in_cart']


class ProductsInCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductsInCart
        fields = '__all__'

    def validate(self, data):
        """One product in cart only can be valid if quantity is more than
        or equal minimum and quantity is a multiple of amount_per_package

        data here are some instances."""

        p = data['product']

        quantity_gte = data['quantity'] >= p.minimum
        quantity_mult = data['quantity'] % p.amount_per_package == 0

        if not quantity_gte:
            msg = f'Minimum quantity of {p.name} is {p.minimum}'
            raise serializers.ValidationError(msg)

        if not quantity_mult:
            amount = p.amount_per_package
            msg = f'Quantity of {p.name} sould be multiple of {amount}'
            raise serializers.ValidationError(msg)

        if data['quantity'] > p.max_availability:
            max_available = p.max_availability
            msg = f'Max disponible quantity of {p.name} is {max_available}'
            raise serializers.ValidationError(msg)

        return data


class ItemsIntoCartSerializer(serializers.ModelSerializer):
    product = serializers.StringRelatedField()
    value = serializers.DecimalField(
        max_digits=10, decimal_places=2)

    class Meta:
        model = ProductsInCart
        fields = ['id', 'product', 'quantity', 'value']

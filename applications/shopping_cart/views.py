from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Sum

from .serializers import (ShoppingCartSerializer,
                          ProductsInCartSerializer,
                          ItemsIntoCartSerializer,)

from .models import ShoppingCart, ProductsInCart


class StartCart(APIView):
    """This view allows to create an empty cart"""

    def get(self, request):
        cart = ShoppingCart.objects.create()

        return Response(ShoppingCartSerializer(cart).data)


class CleanCart(APIView):
    """This view allows to clean cart products"""

    def get(self, request, cart):
        cart = ShoppingCart.objects.get(pk=cart)
        cart.products_clean()

        return Response({'message': 'All items are deleted from cart'})


class CartDetails(APIView):
    """This view only show the cart with details and the total price and
    quantity"""

    def get(self, request, cart):
        cart = ShoppingCart.objects.get(pk=cart)
        items = cart.items_in_cart.all()
        total_quantity = items.aggregate(Sum('quantity'))['quantity__sum']
        total_value = cart.total_value()

        return Response({
            'shopping-cart': ShoppingCartSerializer(cart).data,
            'products': ItemsIntoCartSerializer(items, many=True).data,
            'total-quantity': total_quantity,
            'total-value': total_value})


class AddProductsInCart(APIView):
    """This view allows to products in cart management
    quantity should be greater or equal minimum for product and
    quantity should be multiple of amount_per_package"""

    def post(self, request):
        """Create a new item in the cart"""

        serialized = ProductsInCartSerializer(data=request.data)

        if serialized.is_valid():
            new_product = serialized.save()

            return Response(ProductsInCartSerializer(new_product).data)

        return Response(serialized.errors)


class UpdateQuantityForProduct(APIView):
    """This view allows to change quantity of product in cart"""

    def post(self, request):
        product = ProductsInCart.objects.get(pk=request.data['product'])
        serialized = ProductsInCartSerializer(
            product, data=request.data, partial=True)

        if serialized.is_valid():
            serialized.save()

            return Response(serialized.data)

        return Response(serialized.errors)


class RemoveProductFromCart(APIView):
    """This view removes the product from cart"""

    def post(self, request):
        product = ProductsInCart.objects.get(pk=request.data['product'])
        product.delete()

        return Response({'message': 'Product successfully removed'})

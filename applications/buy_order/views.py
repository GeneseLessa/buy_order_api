from rest_framework.views import APIView
from rest_framework.response import Response

from applications.shopping_cart.models import ShoppingCart

from .models import BuyOrder, ItemsInOrder
from .serializers import BuyOrderSerializer


class CreateAndDetilOrder(APIView):

    def post(self, request):
        cart = ShoppingCart.objects.get(pk=request.data['cart'])
        # print(cart.total_value())

        # creation of Order register
        buy_order = BuyOrder.objects.create(total_price=cart.total_value())
        # put the items into the order with quantities
        for i in cart.items_in_cart.all():
            ItemsInOrder.objects.create(
                order=buy_order,
                product=i.product,
                quantity=i.quantity
            )

        # cleaning the cart
        cart.products_clean()

        serialized = BuyOrderSerializer(buy_order).data

        return Response(serialized)

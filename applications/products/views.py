from typing import OrderedDict
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Product
from .serializers import ProductSerializer


class SearchProduct(APIView):
    """This view is responsible for product search"""

    def get(self, request, name):
        """GET /products/search/<str:name>"""
        products = Product.objects.filter(name__icontains=name)
        serialized = ProductSerializer(products, many=True)

        return Response(serialized.data)

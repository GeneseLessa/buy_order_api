from django.test import TestCase, Client
from faker import Faker
from random import randint

from .models import BuyOrder, ItemsInOrder
from applications.products.models import Product

fake = Faker()


class OrderModelTestCase(TestCase):
    """This test case intended to test some of the fundamental parts of
    buy order endpoint"""

    def setUp(self):
        self.bo = BuyOrder()

    def test_presence_and_consistence_of_fields(self):
        """Basic fields and ID in UUID4"""

        self.assertFalse(self.bo is None)
        self.assertTrue(hasattr(self.bo, 'total_price'))

        self.bo.total_price = 10
        self.bo.save()

        self.assertTrue(self.bo.id is not None)


class ItemsInOrderTestCase(TestCase):
    """This test case only checks the items in order model structure"""

    def setUp(self):
        self.items = ItemsInOrder()

    def test_presence_and_consistence_of_fields(self):
        """Basic fields"""
        self.assertFalse(self.items is None)
        self.assertTrue(hasattr(self.items, 'product'))
        self.assertTrue(hasattr(self.items, 'quantity'))


class OrderEndpointsTestCase(TestCase):
    """This test case is responsible for check basic functionalities of buy
    order endpoint"""

    def setUp(self):
        self.client = Client()

    def test_create_buy_order_address_access(self):
        """POST /shopping/close passing the cart and the its content"""

        # creating a cart
        cart = self.client.get('/shopping/start').json()['id']

        # creating some products
        for i in range(5):
            Product.objects.create(
                name=fake.domain_name(),
                price=randint(20, 50),
                minimum=10,
                amount_per_package=randint(2, 6),
                max_availability=100
            )

        products = Product.objects.all()

        # adding some products into cart
        for i in products:
            self.client.post('/shopping/cart/add_product', {
                'cart': cart,
                'product': i.id,
                'quantity': 10 + i.amount_per_package * 2
            })

        response = self.client.post('/shopping/close', {'cart': cart})

        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(str(response.json()['id'])) > 5)

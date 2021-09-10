from django.test import TestCase, Client
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from faker import Faker
from random import randint, random

from .models import Product

fake = Faker()


class ProductsValidationAndStructureTestCase(TestCase):
    """This is the test case for product model validation rules"""

    def setUp(self):
        self.product = Product()

    def test_fields_existence(self):
        """The following fields should stay in the model structure"""

        self.assertTrue(hasattr(self.product, 'name'))
        self.assertTrue(hasattr(self.product, 'price'))
        self.assertTrue(hasattr(self.product, 'minimum'))
        self.assertTrue(hasattr(self.product, 'amount_per_package'))
        self.assertTrue(hasattr(self.product, 'max_availability'))

    def test_fields_should_not_be_blank(self):
        """The fields name, price, minimum, amount_per_package and
        max_availability shouldn't be blank or null"""

        try:
            self.product.full_clean()

        except ValidationError as e:
            self.assertTrue('name' in e.message_dict)
            self.assertTrue('price' in e.message_dict)
            self.assertTrue('minimum' in e.message_dict)
            self.assertTrue('amount_per_package' in e.message_dict)
            self.assertTrue('max_availability' in e.message_dict)

    def test_all_fields_except_name_shoul_be_positive(self):
        """The model numerical fields should never be less than 0"""

        self.product.name = fake.name()

        self.product.price = -1
        self.product.minimum = -1
        self.product.amount_per_package = -1
        self.product.max_availability = -1

        try:
            self.product.full_clean()

        except ValidationError as e:
            self.assertTrue('price' in e.message_dict)
            self.assertTrue('minimum' in e.message_dict)
            self.assertTrue('amount_per_package' in e.message_dict)
            self.assertTrue('max_availability' in e.message_dict)

    def test_shouldnt_have_two_products_with_the_same_name(self):
        """Each product on the system should have a UNIQUE name"""

        name = fake.name()

        try:
            for i in range(2):
                Product.objects.create(
                    name=name, price=0, minimum=0,
                    amount_per_package=0, max_availability=0)

                self.assertEqual(Product.objects.all().count(), 1)

        except IntegrityError as e:
            self.assertTrue('UNIQUE constraint failed' in e.args[0])

    def test_default_presentation_of_product_is_the_name(self):
        """Default reference for product is the name"""
        self.product.name = 'Farinha de milho'
        self.assertEqual(self.product.__repr__(),
                         '<Product: Farinha de milho>')


class ProductEndpointsTestCase(TestCase):
    """This test case intends to be an endpoint check for functionalities
    described on the challenge rules"""

    def setUp(self):
        self.client = Client()
        names = [
            'ração para cães', 'ração para gatos', 'ração para coelhos',
            'farinha de milho', 'farinha de rosca', 'farinha de mandioca',
        ]
        # creating 6 test products
        for name in names:
            Product.objects.create(
                name=name,
                price=random() * 100,
                minimum=randint(10, 30),
                amount_per_package=randint(1, 10),
                max_availability=200)

    def test_get_product_by_name(self):
        """This endpoint is responsible for return some products by the
        name"""

        response = self.client.get('/products/search/para')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 3)

        response = self.client.get('/products/search/mandio')
        self.assertEqual(len(response.data), 1)

        response = self.client.get('/products/search/a')
        self.assertEqual(len(response.data), 6)

        response = self.client.get('/products/search/»')
        self.assertEqual(len(response.data), 0)

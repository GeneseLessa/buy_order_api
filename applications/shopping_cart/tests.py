from django.test import TestCase, Client
from django.core.exceptions import ObjectDoesNotExist
from faker import Faker
from random import randint

from .models import ShoppingCart, ProductsInCart
from applications.products.models import Product

fake = Faker()


class ShoppingCartTestCase(TestCase):
    """This test case intends to cover model validation"""

    def setUp(self):
        self.cart = ShoppingCart()

    def test_model_and_fields_are_present(self):
        """Warranty that fields and model exists"""

        self.assertFalse(self.cart is None)
        self.assertTrue(hasattr(self.cart, 'is_active'))
        self.assertEqual(self.cart.is_active, True)


class ProductsInCartTestCase(TestCase):
    """This test case intends to cover model validation and process into it"""

    def setUp(self):
        # PIC == Products In Cart
        self.pic = ProductsInCart()

    def test_model_and_fields_are_present(self):
        """Fields and validations tests"""

        self.assertFalse(self.pic is None)
        # in the first moment, the fk fields do not exists
        self.assertFalse(hasattr(self.pic, 'cart'))
        self.assertFalse(hasattr(self.pic, 'product'))

        self.assertTrue(hasattr(self.pic, 'quantity'))


class ShoppingCartEndpointsTestCase(TestCase):
    """This test case is responsible for cover the shopping cart endpoints"""

    def setUp(self):
        self.client = Client()
        self.product = Product.objects.create(
            name=fake.domain_word(),
            price=50,
            minimum=10,
            amount_per_package=5,
            max_availability=50)

    def test_creating_shopping_cart(self):
        """Trying to create and endpoint and return the cart id for shopping"""

        response = self.client.get('/shopping/start')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['id'], 1)

    def test_clean_items_into_cart(self):
        """Cheking if the endpoint can clean a cart when it is called"""

        self.client.get('/shopping/start')
        cart = ShoppingCart.objects.first()

        response = self.client.get(f'/shopping/cart/{cart.id}/clean')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(cart.items_in_cart.all()), 0)

    def test_add_a_product_into_a_cart(self):
        """Add a product with some quantity to a cart"""

        # creating a cart
        cart = self.client.get('/shopping/start').json()['id']

        response = self.client.post('/shopping/cart/add_product', {
            'cart': cart,
            'product': self.product.id,
            'quantity': 15
        })

        cart = ShoppingCart.objects.get(pk=cart)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(cart.items_in_cart.all()), 1)

    def test_change_product_in_cart(self):
        """Change product quantity in cart"""

        cart = self.client.get('/shopping/start').json()['id']
        new_product = self.client.post('/shopping/cart/add_product', {
            'cart': cart,
            'product': self.product.id,
            'quantity': 15
        })

        # changing the quantity in new product from 15 to 5 (down the minimum)
        response = self.client.post('/shopping/cart/change_product', {
            'product': new_product.json()['id'],
            'quantity': 5
        })

        self.assertEqual(response.status_code, 200)

        # taking again the instance
        new_product = ProductsInCart.objects.get(pk=new_product.json()['id'])
        self.assertEqual(new_product.quantity, 15)

        # changing the quantity in new product from 15 to 10 (the minimum)
        response = self.client.post('/shopping/cart/change_product', {
            'product': new_product.id,
            'quantity': 10
        })

        # taking again the instance
        new_product = ProductsInCart.objects.get(pk=new_product.id)
        self.assertEqual(new_product.quantity, 10)

    def test_remove_a_product_from_cart(self):
        """Remove a product from cart"""

        # creating a cart
        cart = self.client.get('/shopping/start').json()['id']

        product = self.client.post('/shopping/cart/add_product', {
            'cart': cart,
            'product': self.product.id,
            'quantity': 15
        }).json()['id']

        # removing the product into the cart
        response = self.client.post(
            '/shopping/cart/remove_product', {'product': product})

        self.assertEqual(response.status_code, 200)

        try:
            ProductsInCart.objects.get(pk=product)
        except ObjectDoesNotExist as e:
            msg = 'matching query does not exist'
            self.assertTrue(msg in e.args[0])

    def test_see_all_products_in_cart(self):
        """This view returns a JSON with all of the cart products and total
        price of them."""

        # creating a cart
        cart = self.client.get('/shopping/start').json()['id']

        # creating some products
        for i in range(2):
            Product.objects.create(
                name=f'{fake.domain_word()}{fake.name()}',
                price=randint(30, 70),
                minimum=randint(2, 5),
                amount_per_package=randint(1, 30),
                max_availability=randint(600, 20000))

        products = Product.objects.all()

        # creating products in cart using the endpoint for that
        for i in products:
            self.client.post('/shopping/cart/add_product', {
                'cart': cart,
                'product': i.id,
                'quantity': randint(i.minimum, 100)
            })

        response = self.client.get(f'/shopping/cart/{cart}/details')

        self.assertEqual(response.status_code, 200)

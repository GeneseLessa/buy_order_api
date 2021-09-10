from django.contrib import admin
from django.urls import path

from applications.products.views import SearchProduct
from applications.shopping_cart.views import (StartCart,
                                              CleanCart,
                                              CartDetails,
                                              AddProductsInCart,
                                              UpdateQuantityForProduct,
                                              RemoveProductFromCart,)

from applications.buy_order.views import CreateAndDetilOrder

urlpatterns = [
    path('admin/', admin.site.urls),

    # products
    path('products/search/<str:name>', SearchProduct.as_view()),

    # shopping cart and product actions
    path('shopping/start', StartCart.as_view()),
    path('shopping/cart/<int:cart>/clean', CleanCart.as_view()),
    path('shopping/cart/add_product',
         AddProductsInCart.as_view()),
    path('shopping/cart/change_product',
         UpdateQuantityForProduct.as_view()),
    path('shopping/cart/remove_product',
         RemoveProductFromCart.as_view()),
    path('shopping/cart/<int:cart>/details',
         CartDetails.as_view()),

    # creating and detail order
    path('shopping/close', CreateAndDetilOrder.as_view()),
]

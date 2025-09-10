from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_view, name='cart_view'),
    path('checkout/<int:product_id>/', views.create_checkout_session, name='checkout'),
    path('create-order/', views.create_order, name='create_order'),
    path('orders/', views.order_list, name='order_list'),
]

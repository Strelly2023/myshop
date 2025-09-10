from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Product, Category, CartItem, Order, OrderItem
from django.conf import settings
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY

def product_list(request):
    category_id = request.GET.get('category')
    products = Product.objects.filter(category_id=category_id) if category_id else Product.objects.all()
    categories = Category.objects.all()
    return render(request, 'catalog/product_list.html', {'products': products, 'categories': categories})

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'catalog/product_detail.html', {'product': product})

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)
    if not created:
        cart_item.quantity += 1
    cart_item.save()
    return redirect('cart_view')

@login_required
def cart_view(request):
    cart_items = CartItem.objects.filter(user=request.user)
    return render(request, 'catalog/cart.html', {'cart_items': cart_items})

@login_required
def create_checkout_session(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'usd',
                'product_data': {'name': product.name},
                'unit_amount': int(product.price * 100),
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url='http://localhost:8000/orders/',
        cancel_url='http://localhost:8000/',
    )
    return redirect(session.url, code=303)

@login_required
def create_order(request):
    cart_items = CartItem.objects.filter(user=request.user)
    if not cart_items.exists():
        return redirect('product_list')
    total = sum(item.total_price() for item in cart_items)
    order = Order.objects.create(user=request.user, total_amount=total)
    for item in cart_items:
        OrderItem.objects.create(order=order, product=item.product, quantity=item.quantity, price=item.product.price)
    cart_items.delete()
    return redirect('order_list')

@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'catalog/order_list.html', {'orders': orders})

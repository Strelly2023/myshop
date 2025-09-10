from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from .models import Category, Product, CartItem, Order, OrderItem
import uuid

def index(request):
    categories = Category.objects.all()
    return render(request, 'catalog/index.html', {'categories': categories})

def category_page(request, category_id):
    categories = Category.objects.all()
    selected_category = get_object_or_404(Category, id=category_id)
    products = Product.objects.filter(category=selected_category)
    return render(request, 'catalog/category_page.html', {
        'categories': categories,
        'selected_category': selected_category,
        'products': products
    })

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
    return redirect('view_cart')

@login_required
def view_cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    return render(request, 'catalog/cart.html', {'cart_items': cart_items})

@login_required
def update_cart(request):
    if request.method == 'POST':
        for item_id, quantity in request.POST.items():
            if item_id.startswith('quantity_'):
                cart_item_id = int(item_id.split('_')[1])
                cart_item = CartItem.objects.get(id=cart_item_id, user=request.user)
                cart_item.quantity = int(quantity)
                cart_item.save()
    return redirect('view_cart')

@login_required
def checkout(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total = sum(item.total_price() for item in cart_items)
    if request.method == 'POST':
        reference = str(uuid.uuid4())[:8]
        order = Order.objects.create(user=request.user, total_amount=total, reference=reference)
        for item in cart_items:
            OrderItem.objects.create(order=order, product=item.product, quantity=item.quantity, price=item.product.price)
        cart_items.delete()
        send_mail(
            subject='Order Confirmation',
            message=f'Thank you for your order #{order.reference}. Total: ${order.total_amount}',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[request.user.email],
        )
        return redirect('order_confirmation', order_id=order.id)
    return render(request, 'catalog/checkout.html', {'cart_items': cart_items, 'total': total})

@login_required
def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'catalog/order_confirmation.html', {'order': order})

from django.shortcuts import render, redirect, get_object_or_404
from products.models import Product
from .models import Cart, CartItem
from django.contrib import messages
# Create your views here.


def view_cart(request):
    """ A view that renders the cart contents page """
    
    return render(request, 'cart/cart.html')


def _cart_id(request):
    """ A private function to get the cart id from the current session or create a new session """

    cart = request.session.session_key  # Get the session id
    if not cart:
        # Create a new session if there is no session available
        cart = request.session.create()
    return cart


def add_to_cart(request, product_id):
    """ A view that manages add items to the cart
        and products variation 
     """
    
    product = Product.objects.get(id=product_id)

    try:
        # get the cart using the cart id present in the session
        cart = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            # Create a new cart if there is no cart session created
            cart_id=_cart_id(request)
        )
    cart.save()

    try:
        cart_item = CartItem.objects.get(product=product)
        cart_item.quantity += 1
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(
            product=product,
            quantity=1,
            cart=cart,
        )
        cart_item.save()
    return redirect('view_cart')


def remove_from_cart(request, product_id, cart_item_id):
    """ A view to decrese items number from the cart """

    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    try:
        cart_item = CartItem.objects.get(
            product=product, cart=cart, id=cart_item_id)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
            messages.success(
                request, f'Removed {product.name} from your cart!')

        else:
            cart_item.delete()
            messages.success(
                request, f'Removed {product.name} from your cart!')
    except Exception as e:
        messages.error(request, f'Error removing item: {e} from your cart!')
    return redirect('view_cart')


def remove_cart_item(request, product_id, cart_item_id):
    """ A view to remove items from the cart """

    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(
        product=product, cart=cart, id=cart_item_id)
    cart_item.delete()
    messages.success(request, f'Removed {product.name} from your cart!')
    return redirect('view_cart')
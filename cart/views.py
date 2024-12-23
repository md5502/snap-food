from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from food.models import Food
from orders.models import Order, OrderItem, OrderStatus
from users.models import Address


# Utility function to calculate total price
def calculate_total(cart):
    return sum(item["total"] for item in cart.values())


@require_POST
def add_to_cart(request, product_id):
    product = get_object_or_404(Food, pk=product_id)
    cart = request.session.get("cart", {})

    if str(product_id) in cart:
        if product.count >= cart[str(product_id)]["quantity"]:
            # TODO: user will know the items count
            message = "cant add more than the Item quantity in the store"
            messages.success(request, message)
            return redirect(request.META.get("HTTP_REFERER", "/"))
        cart[str(product_id)]["quantity"] += 1
        cart[str(product_id)]["total"] = cart[str(product_id)]["quantity"] * cart[str(product_id)]["price"]
        message = "Item quantity updated"
        messages.success(request, message)
    else:
        cart[str(product_id)] = {
            "name": product.name,
            "quantity": 1,
            "pk": str(product_id),
            "price": float(product.price),
            "total": float(product.price),
        }

    request.session["cart"] = cart
    message = "Item added to the cart"
    messages.success(request, message)
    return redirect(request.META.get("HTTP_REFERER", "/"))


@require_POST
def remove_from_cart(request, product_id):
    cart = request.session.get("cart", {})

    if str(product_id) in cart:
        del cart[str(product_id)]
        request.session["cart"] = cart
        message = "Item removed from cart"
        messages.debug(request, message)

    return redirect(request.META.get("HTTP_REFERER", "/"))


@require_POST
def decrease_quantity(request, product_id):
    cart = request.session.get("cart", {})

    if str(product_id) in cart:
        if cart[str(product_id)]["quantity"] > 1:
            cart[str(product_id)]["quantity"] -= 1
            cart[str(product_id)]["total"] = cart[str(product_id)]["quantity"] * cart[str(product_id)]["price"]
            message = "Item quantity decreased"
            messages.debug(request, message)
        else:
            del cart[str(product_id)]
            message = "Item removed from cart"
            messages.debug(request, message)
    else:
        message = "Item not found in cart"
        messages.debug(request, message)

    request.session["cart"] = cart
    return redirect(request.META.get("HTTP_REFERER", "/"))


def view_cart(request):
    cart = request.session.get("cart", {})
    total_price = calculate_total(cart)

    return render(request, "cart/cart.html", {"cart": cart, "total_price": total_price})


@require_POST
def clear_cart(request):
    request.session["cart"] = {}
    message = "Cart cleared"
    messages.success(request, message)

    return render(request, "cart/cart.html", {"cart": {}, "total_price": 0})



def checkout(request):
    cart = request.session.get("cart", {})
    if cart == {}:
        messages.error(request, "cart is empty")
        return redirect("cart:view_cart")
    if not request.user.addresses.exists():
        messages.warning(request, "You need to add at least one address to receive the foods.")
        return redirect("users:create_address")
    if request.method == "POST":
        address_pk = request.POST.get("address", "")
        if not address_pk:
            messages.error(request, "Please select an address.")
            return redirect(request.META.get("HTTP_REFERER", "/"))

        address_object = get_object_or_404(Address, pk=address_pk)
        order, created = Order.objects.get_or_create(
            user=request.user,
            status=OrderStatus.PENDING,
            defaults={"shipping_address": address_object},
        )

        order_items = []
        for item_id, details in cart.items():
            food = get_object_or_404(Food, pk=item_id)
            quantity = details["quantity"]

            if quantity > food.count:
                messages.warning(request, f"We only have {food.count} of {food.name}. Please adjust your order.")
                return redirect(request.META.get("HTTP_REFERER", "/"))

            order_items.append(OrderItem(order=order, product=food, quantity=quantity, unit_price=food.price))

        OrderItem.objects.bulk_create(order_items)
        request.session["cart"] = {}

        messages.success(request, "Order created successfully!")
        order.status = OrderStatus.PROCESSING
        order.save()
        return redirect("cart:view_cart")

    total_price = calculate_total(cart)
    return render(request, "cart/checkout.html", {"cart": cart, "total_price": total_price})

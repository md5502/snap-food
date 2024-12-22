from django.http import JsonResponse
from django.shortcuts import render

from food.models import Food


def add_to_cart(request, product_id):
    product = Food.objects.filter(pk=product_id).first()

    if not product:
        return JsonResponse({"message": "Product not found"})

    cart = request.session.get("cart", {})

    if str(product_id) in cart:
        cart[str(product_id)]["quantity"] += 1
        cart[str(product_id)]["total"] = cart[str(product_id)]["quantity"] * cart[str(product_id)]["price"]

        message = "Item quantity updated"
    else:
        cart[str(product_id)] = {
            "name": product.name,
            "quantity": 1,
            "pk": str(product_id),
            "price": float(product.price),
            "total": float(product.price),
        }
        message = "Item added to cart"

    request.session["cart"] = cart
    return render(
        request,
        "cart/cart.html",
        {"cart": cart, "total_price": sum(item["total"] for item in cart.values()), "message": message},
    )


def remove_from_cart(request, product_id):
    cart = request.session.get("cart", {})

    if str(product_id) in cart:
        del cart[str(product_id)]
        request.session["cart"] = cart
        message = "Item removed from cart"
    else:
        message = "Item not found in cart"

    return render(
        request,
        "cart/cart.html",
        {"cart": cart, "total_price": sum(item["total"] for item in cart.values()), "message": message},
    )


def decrease_quantity(request, product_id):
    cart = request.session.get("cart", {})

    if str(product_id) in cart:
        if cart[str(product_id)]["quantity"] > 1:
            cart[str(product_id)]["quantity"] -= 1
            cart[str(product_id)]["total"] = cart[str(product_id)]["quantity"] * cart[str(product_id)]["price"]
            message = "Item quantity decreased"
        else:
            del cart[str(product_id)]
            message = "Item removed from cart"
    else:
        message = "Item not found in cart"

    request.session["cart"] = cart
    return render(
        request,
        "cart/cart.html",
        {"cart": cart, "total_price": sum(item["total"] for item in cart.values()), "message": message},
    )


def view_cart(request):
    cart = request.session.get("cart", {})
    total_price = sum(item["total"] for item in cart.values())

    message = "Here is your shopping cart"
    return render(request, "cart/cart.html", {"cart": cart, "total_price": total_price, "message": message})


def clear_cart(request):
    request.session["cart"] = {}
    message = "Cart cleared"
    return render(request, "cart/cart.html", {"cart": {}, "total_price": 0, "message": message})

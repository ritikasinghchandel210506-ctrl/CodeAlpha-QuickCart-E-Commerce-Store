from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from .models import Product, Order, OrderItem
from .forms import RegisterForm


def home(request):
    products = Product.objects.all()
    return render(request, "store/home.html", {"products": products})


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, "store/product_detail.html", {"product": product})


def add_to_cart(request, pk):
    cart = request.session.get("cart", {})
    if isinstance(cart, list):
        cart = {}
    pk = str(pk)

    if pk in cart:
        cart[pk] = int(cart[pk]) + 1
    else:
        cart[pk] = 1

    request.session["cart"] = cart
    request.session.modified = True
    return redirect("cart")


def decrease_quantity(request, pk):
    cart = request.session.get("cart", {})
    pk = str(pk)

    if pk in cart:
        cart[pk] = int(cart[pk]) - 1
        if cart[pk] <= 0:
            del cart[pk]

    request.session["cart"] = cart
    request.session.modified = True
    return redirect("cart")


def remove_from_cart(request, pk):
    cart = request.session.get("cart", {})
    pk = str(pk)

    if pk in cart:
        del cart[pk]

    request.session["cart"] = cart
    request.session.modified = True
    return redirect("cart")


def cart_view(request):
    cart = request.session.get("cart", {})

    items = []
    total = 0

    for product_id, quantity in cart.items():

        product = Product.objects.get(id=product_id)

        subtotal = product.price * quantity

        items.append({
            "product": product,
            "quantity": quantity,
            "subtotal": subtotal
        })

        total += subtotal

    return render(
        request,
        "store/cart.html",
        {
            "items": items,
            "total": total
        }
    )


def checkout(request):

    cart = request.session.get("cart", {})

    if not cart:
        return redirect("cart")

    if request.user.is_authenticated:

        order = Order.objects.create(user=request.user)

        for product_id, quantity in cart.items():

            product = Product.objects.get(id=product_id)

            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity
            )

        request.session["cart"] = {}

    return render(request, "store/checkout.html")

def register(request):
    form = RegisterForm()

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("/")

    return render(request, "store/register.html", {"form": form})


def logout_user(request):
    logout(request)
    return redirect("/")
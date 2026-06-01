from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Order, OrderItem
from .forms import RegisterForm
from django.contrib.auth import login
from django.contrib.auth import logout
from django.shortcuts import redirect

cart = []

def home(request):
    products = Product.objects.all()
    return render(request, "store/home.html", {"products": products})


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, "store/product_detail.html", {"product": product})


def add_to_cart(request, pk):
    cart.append(pk)
    return redirect("cart")

def remove_from_cart(request, pk):
    cart = request.session.get('cart', [])

    if str(pk) in cart:
        cart.remove(str(pk))

    request.session['cart'] = cart

    return redirect('cart')

def cart_view(request):
    products = Product.objects.filter(id__in=cart)
    return render(request, "store/cart.html", {"products": products})


def checkout(request):
    if request.user.is_authenticated:
        order = Order.objects.create(user=request.user)

        for item in cart:
            product = Product.objects.get(id=item)
            OrderItem.objects.create(order=order, product=product)

        cart.clear()

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
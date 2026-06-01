from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("product/<int:pk>/", views.product_detail, name="product"),
    path("add/<int:pk>/", views.add_to_cart, name="add"),
    path("cart/", views.cart_view, name="cart"),
    path("checkout/", views.checkout, name="checkout"),
    path("register/", views.register, name="register"),
    path("logout/", views.logout_user, name="logout"),
    path('remove/<int:pk>/', views.remove_from_cart, name='remove_from_cart'),
]

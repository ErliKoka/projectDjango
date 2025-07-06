from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="homePage"),
    path("about/", views.about, name="aboutPage"),
    path("contact/", views.contact, name="contactPage"),
    path("gallery/", views.gallery, name="galleryPage"),
    path("detailitem/<int:id>/", views.detailitem, name="detailitemPage"),
    path('categoryDetail/<slug:slug>/', views.categoryPage, name="categoryPage"),  
    path('register/', views.register, name="register"),
    path('login/', views.loginA, name="login"),
    path('logout/', views.logoutT, name="logout"),
    path('add-to-cart/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_view, name='cart'),
    path('update-cart/', views.update_cart, name='update_cart'),
    path('remove-from-cart/', views.remove_from_cart, name='remove_from_cart'),
    path('search/', views.search_view, name='search'),
    path('checkout/', views.checkout_view, name='checkout'),
    path('checkout-success/', views.checkout_success, name='checkout_success'),


]

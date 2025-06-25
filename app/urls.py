from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="homePage"),
    path("about/", views.about, name="aboutPage"),
    path("contact/", views.contact, name="contactPage"),
    path("gallery/", views.gallery, name="galleryPage"),
    path("detailitem/<id>/", views.detailitem, name="detailitemPage"),
    path("categoryDetail/<slug>", views.categoryPage, name="categoryPage"),
    path('register/', views.register, name="register"),
    path('login/', views.loginA, name="login"),
    path('logout/', views.logoutT, name="logout"),
]
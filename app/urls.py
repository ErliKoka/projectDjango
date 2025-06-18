from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="homePage"),
    path("about/", views.about, name="aboutPage"),
    path("contact/", views.contact, name="contactPage"),
    path("gallery/", views.gallery, name="galleryPage"),
]
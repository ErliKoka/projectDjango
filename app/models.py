from django.db import models

# Create your models here.
# burra, gra
class Category(models.Model):
    category_slug = models.SlugField(unique=True, primary_key=True)
    category_name = models.CharField(max_length=200, null=True, blank=True)
    category_image = models.ImageField(upload_to="category/", null=True, blank=True)
    category_description = models.TextField(max_length=2000, null=True, blank=True)

    def __str__(self):
        return f"{self.category_name}"

#eshte per koleksionin
class Collection(models.Model):
    collection_slug = models.SlugField(unique=True, primary_key=True)
    collection_name = models.CharField(max_length=200, null=True, blank=True)
    collection_image = models.ImageField(upload_to="collection/", null=True, blank=True)
    

    def __str__(self):
        return f"{self.collection_name}"


# syzet
class Item(models.Model):
    item_name = models.CharField(max_length=100, null=True, blank=True)
    item_description = models.TextField(max_length=2000, null=True, blank=True)
    item_image = models.ImageField(upload_to="item/",null=True, blank=True)
    item_price = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    item_category = models.ForeignKey(
        Category, on_delete=models.CASCADE, null=True, blank=True
    )
    item_collection = models.ForeignKey(
        Collection, on_delete=models.CASCADE, null=True, blank=True
     )
    def __str__(self):
        return f"{self.item_name}"

class Contact(models.Model):
    contact_name = models.CharField(max_length=100, null=True, blank=True)
    contact_surname = models.CharField(max_length=100, null=True, blank=True)
    contact_comment = models.TextField(max_length=2000, null=True, blank=True)
    contact_email = models.EmailField(null=True, blank=True)

    def __str__(self):
        return f"{self.contact_name} {self.contact_surname}"
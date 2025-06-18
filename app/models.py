from django.db import models

# Create your models here.
class Item(models.Model):
    item_name = models.CharField(max_length=100, null=True, blank=True)
    item_description = models.TextField(max_length=2000, null=True, blank=True)
    item_image = models.ImageField(upload_to="item/",null=True, blank=True)

    def __str__(self):
        return f"{self.item_name}"

class Contact(models.Model):
    contact_name = models.CharField(max_length=100, null=True, blank=True)
    contact_surname = models.CharField(max_length=100, null=True, blank=True)
    contact_comment = models.TextField(max_length=2000, null=True, blank=True)
    contact_email = models.EmailField(null=True, blank=True)

    def __str__(self):
        return f"{self.contact_name} {self.contact_surname}"
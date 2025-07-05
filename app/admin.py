from django.contrib import admin
from .models import Item, Contact, Category, Collection

# Customizing Item admin
class ItemAdmin(admin.ModelAdmin):
    list_display = ('item_name', 'item_price', 'item_category', 'featured')  # Display 'featured' field in list view
    list_filter = ('featured', 'item_category')  # Filter items by 'featured' and 'item_category'
    search_fields = ('item_name', 'item_category__category_name')  # Search by item name or category name
    # Fields to be displayed in the form when adding/editing an item
    fieldsets = (
        (None, {
            'fields': ('item_name', 'item_description', 'item_image', 'item_price', 'item_category', 'item_collection', 'featured')
        }),
    )
    # Making the 'featured' field visible and editable in the list display and filters
    ordering = ('-featured',)  # Optionally, you can order items by their featured status (featured items first)

# Registering the models with the customized admin
admin.site.register(Item, ItemAdmin)
admin.site.register(Contact)
admin.site.register(Category)
admin.site.register(Collection)

from django.contrib import admin
from .models import Item, Contact, Category, Collection


class ItemAdmin(admin.ModelAdmin):
    list_display = ('item_name', 'item_price', 'item_category', 'featured')  
    list_filter = ('featured', 'item_category')  
    search_fields = ('item_name', 'item_category__category_name')  
    
    fieldsets = (
        (None, {
            'fields': ('item_name', 'item_description', 'item_image', 'item_price', 'item_category', 'item_collection', 'featured')
        }),
    )
    
    ordering = ('-featured',)  


admin.site.register(Item, ItemAdmin)
admin.site.register(Contact)
admin.site.register(Category)
admin.site.register(Collection)

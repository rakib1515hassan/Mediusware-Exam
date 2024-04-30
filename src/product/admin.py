from django.contrib import admin
from product.models import *


# Register your models here.
# admin.site.register(Product)
admin.site.register(Variant)
admin.site.register(ProductVariant)
admin.site.register(ProductImage)
admin.site.register(ProductVariantPrice)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'sku', 'description']

from django.db import models
from config.g_model import TimeStampMixin
from django.utils import timezone

# Create your models here.
class Variant(TimeStampMixin):
    title = models.CharField(max_length=40, unique=True)
    description = models.TextField()
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class Product(TimeStampMixin):
    title = models.CharField(max_length=255)
    sku   = models.SlugField(max_length=255, unique=True)
    description = models.TextField()

    def __str__(self):
        return self.title


class ProductImage(TimeStampMixin):
    def product_image_path(instance, filename):
        timestamp = timezone.now().strftime('%Y%m%d%H%M%S')
        return f'ProductImage/{instance.product.title}/{timestamp}_{filename}'

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    file_path = models.ImageField(upload_to=product_image_path)

    def __str__(self):
        return f"ID={self.id} -> {self.product.title}"


class ProductVariant(TimeStampMixin):
    variant_title = models.CharField(max_length=255)
    variant = models.ForeignKey(Variant, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f"ID={self.id}, {self.variant.title} -> {self.variant_title}"


class ProductVariantPrice(TimeStampMixin):
    product_variant_one   = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, null=True,
                                            related_name='product_variant_one')
    product_variant_two   = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, null=True,
                                            related_name='product_variant_two')
    product_variant_three = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, null=True,
                                              related_name='product_variant_three')
    price   = models.FloatField()
    stock   = models.FloatField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f" id={self.id} -> {self.product.title}"

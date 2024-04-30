from rest_framework import serializers
from product.models import Variant, Product, ProductImage, ProductVariant, ProductVariantPrice
from collections import defaultdict


class VariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Variant
        fields = '__all__'

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'file_path']

class ProductVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariant
        fields = ['id', 'variant_title', 'variant', 'product']


class ProductVariantPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariantPrice
        fields = ['product_variant_one', 'product_variant_two', 'product_variant_three', 'price', 'stock']


class ProductRetrieveSerializer(serializers.ModelSerializer):
    product_images = ProductImageSerializer(many=True, read_only=True)
    product_variant_prices = ProductVariantPriceSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'title', 'sku', 'description', 'product_images', 'product_variant_prices']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        
        # Retrieve and serialize product images
        product_images = instance.productimage_set.all()
        representation['product_images'] = ProductImageSerializer(product_images, many=True).data



        # Retrieve and serialize product variants
        product_variants = instance.productvariant_set.all()



        # Organize product variants by their positions
        variants_by_position = defaultdict(list)

        for product_variant in product_variants:
            position = f"{product_variant.variant.id}-{product_variant.variant.title}"
            variants_by_position[position].append({
                'id': product_variant.id,
                'variant_title': product_variant.variant_title
            })

        representation['product_variant'] = dict(variants_by_position)
        


        # Retrieve and serialize product variant prices
        product_variant_prices = instance.productvariantprice_set.all()
        representation['product_variant_prices'] = ProductVariantPriceSerializer(product_variant_prices, many=True).data
        
        return representation
    


class ProductUpdateSerializer(serializers.ModelSerializer):
    product_images = serializers.ListField(
        child = serializers.ImageField(allow_null=True),
        write_only = True,
        required   = False
    )
    variants = serializers.ListField(child=serializers.DictField(), write_only=True, required=False)
    prices   = serializers.ListField(child=serializers.DictField(), write_only=True, required=False)

    class Meta:
        model = Product
        fields = ['title', 'sku', 'description', 'product_images', 'variants', 'prices']

    def update(self, instance, validated_data):
        variants_data = validated_data.pop('variants', [])
        images_data = validated_data.pop('product_images', [])
        prices_data = validated_data.pop('prices', [])

        # Update Product instance fields
        instance.title = validated_data.get('title', instance.title)
        instance.sku   = validated_data.get('sku', instance.sku)
        instance.description = validated_data.get('description', instance.description)
        instance.save()

        # Update ProductVariant instances
        for variant_data in variants_data:
            variant_id = variant_data['variant']
            variant_instance = Variant.objects.get(id=variant_id)

            for variant_title in variant_data['variant_title']:
                ProductVariant.objects.update_or_create(
                    product=instance,
                    variant=variant_instance,
                    variant_title=variant_title
                )

        # Update ProductVariantPrice instances
        for price_data in prices_data:
            title_parts = price_data['title'].split('/')

            pv1 = ProductVariant.objects.filter(product=instance, variant_title=title_parts[0]).first()
            pv2 = ProductVariant.objects.filter(product=instance, variant_title=title_parts[1]).first() if len(
                title_parts) > 1 else None
            pv3 = ProductVariant.objects.filter(product=instance, variant_title=title_parts[2]).first() if len(
                title_parts) > 2 else None

            ProductVariantPrice.objects.update_or_create(
                product =instance,
                product_variant_one   = pv1,
                product_variant_two   = pv2,
                product_variant_three = pv3,
                defaults={'price': price_data['price'], 'stock': price_data['stock']}
            )

        return instance




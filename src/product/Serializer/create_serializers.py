from rest_framework import serializers
from product.models import Variant, Product, ProductImage, ProductVariant, ProductVariantPrice


class ProductSerializer(serializers.ModelSerializer):
    product_images = serializers.ListField(
        child = serializers.ImageField(allow_null=True),
        write_only = True,
        required = False
    )
    variants = serializers.ListField(child=serializers.DictField(), write_only=True)
    prices   = serializers.ListField(child=serializers.DictField(), write_only=True)

    class Meta:
        model = Product
        fields = ['title', 'sku', 'description', 'product_images', 'variants', 'prices']

    def create(self, validated_data):
        request = self.context.get('request')

        variants_data = validated_data.pop('variants')
        images_data = validated_data.pop('product_images', [])
        prices_data = validated_data.pop('prices')


        ## Create Product instance
        product = Product.objects.create(**validated_data)



        ## Create ProductVariant instances
        variant_instances = []

        for variant_data in variants_data:
            variant_id = variant_data['variant']
            variant_instance = Variant.objects.get(id=variant_id)

            for variant_title in variant_data['variant_title']:
                variant_instance_ = ProductVariant.objects.create(
                    product = product,
                    variant = variant_instance,
                    variant_title = variant_title
                )
                variant_instances.append(variant_instance_)



        ## Create ProductVariantPrice instances
        for price_data in prices_data:
            title_parts = price_data['title'].split('/')

            pv1 = ProductVariant.objects.filter(product=product, variant_title=title_parts[0]).first()
            pv2 = ProductVariant.objects.filter(product=product, variant_title=title_parts[1]).first() if len(title_parts) > 1 else None
            pv3 = ProductVariant.objects.filter(product=product, variant_title=title_parts[2]).first() if len(title_parts) > 2 else None

            ProductVariantPrice.objects.create(
                product = product,
                product_variant_one   = pv1,
                product_variant_two   = pv2,
                product_variant_three = pv3,
                
                price = price_data['price'],
                stock = price_data['stock']
            )

        return product



















# class ProductSerializer(serializers.ModelSerializer):
  
#     product_images = serializers.ListField(
#         child=serializers.ImageField(allow_null=True),  
#         write_only=True,
#         required=False  
#     )

#     variants = serializers.ListField(child=serializers.DictField(), write_only=True)
#     prices   = serializers.ListField(child=serializers.DictField(), write_only=True)

#     class Meta:
#         model = Product
#         fields = ['title', 'sku', 'description', 'product_images', 'variants', 'prices']

#     def create(self, validated_data):
#         request = self.context.get('request')

#         variants_data = validated_data.pop('variants')
#         images_data = validated_data.pop('product_images', [])
#         prices_data = validated_data.pop('prices')

#         print("-------------------")
#         print("Request Data =", request.data)
#         print("-------------------")
#         print("variants_data =", variants_data)
#         print("-------------------")
#         print("images_data =", images_data)
#         print("-------------------")
#         print("prices_data =", prices_data)
#         print("-------------------")


#         # product = Product.objects.create(**validated_data)

#         # # Create product images
#         # if images_data:
#         #     for image_data in images_data:
#         #         ProductImage.objects.create(product=product, file_path=image_data)


#         # # Create product variants
#         # if variants_data:
#         #     for variant_data in variants_data:
#         #         variant_title = variant_data['variant_title']
#         #         variant_id = variant_data['variant']

#         #         try:
#         #             variant_obj = Variant.objects.get(id=variant_id)
#         #         except Variant.DoesNotExist:
#         #             pass

#         #         ProductVariant.objects.create(product=product, variant=variant_obj, variant_title = variant_title)



#         # # Create product variant prices
#         # if prices_data:
#         #     for price_data in prices_data:

#         #         variant_titles = [price_data[f'variant_{i}'] for i in range(1, 4)]

#         #         product_variants = ProductVariant.objects.filter(product=product, variant_title__in=variant_titles)
 
#         #         if len(product_variants) == 3: 
#         #             ProductVariantPrice.objects.create(
#         #                 product=product,
#         #                 product_variant_one=product_variants[0],
#         #                 product_variant_two=product_variants[1],
#         #                 product_variant_three=product_variants[2],
#         #                 price=price_data['price'],
#         #                 stock=price_data['stock']
#         #             )
#         #         else:
#         #             pass 
#         return "Success"
        
        





from django.views import generic
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import Http404
from django.db.models import Count, Prefetch
from django.shortcuts import get_object_or_404

from rest_framework import generics
from django.db.models import Q

from product.models import Variant, Product, ProductVariant
from product.Serializer.create_serializers import ProductSerializer
from product.Serializer.update_serializers import ProductRetrieveSerializer, VariantSerializer, ProductUpdateSerializer
from product.utils import api_success, api_error



class CreateProductView(generic.TemplateView):
    template_name = 'products/create.html'

    def get_context_data(self, **kwargs):
        context = super(CreateProductView, self).get_context_data(**kwargs)
        variants = Variant.objects.filter(active=True).values('id', 'title')
        context['product'] = True
        context['variants'] = list(variants.all().distinct())
        return context
    

    
class UpdateProductView(generic.UpdateView):
    template_name = 'products/update.html'
    model  = Product
    fields = ['title', 'sku', 'description']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        variants = Variant.objects.filter(active=True).values('id', 'title')
        context['product']  = get_object_or_404(Product, pk=self.kwargs['pk'])
        context['variants'] = list(variants)
        return context
    



class ProductListView(generic.TemplateView):
    template_name = 'products/list.html'
    products_per_page = 2

    def get_queryset(self):

        filter_string = {}
        product_title   = self.request.GET.get("title", "")
        product_variant = self.request.GET.get("variant", "")
        price_from = self.request.GET.get("price_from", "")
        price_to   = self.request.GET.get("price_to", "")
        date = self.request.GET.get("date", "")

        if product_title:
            filter_string["title__icontains"] = product_title

        if product_variant:
            filter_string["productvariant__variant_title__icontains"] = product_variant

        if date:
            filter_string["created_at__date"] = date

        if price_from and price_to:
            filter_string["productvariantprice__price__range"] = ( price_from, price_to)
            
        queryset = Product.objects.filter(**filter_string).order_by("-created_at")
        return queryset.distinct()

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        queryset = self.get_queryset()

        unique_titles = {} 
        product_variant_list = []

        variants = Variant.objects.filter(active=True).prefetch_related(
            Prefetch('productvariant_set', queryset=ProductVariant.objects.select_related('variant'))
        )

        product_variant_list = [
            {
                "title": variant.title,
                "product_variant": set(product_variant.variant_title for product_variant in variant.productvariant_set.all())
            }
            for variant in variants
        ]

        paginator = Paginator(queryset, self.products_per_page)
        page_number = self.request.GET.get('page')

        try:
            page_obj = paginator.get_page(page_number)
        except EmptyPage:
            raise Http404("Page not found")
        
        context['page_obj'] = page_obj
        context["variants"] = product_variant_list
        context['products_count'] = queryset.count()
        return context
    



class ProductVariantListAPIView(generics.ListAPIView):
    serializer_class = VariantSerializer

    def get_queryset(self):
        return Variant.objects.filter(active = True)





class ProductCreateAPIView(generics.CreateAPIView):
    serializer_class = ProductSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return api_success(serializer.data, status=201, message="Product Create Successfully.")
        
        return api_error({'errors': serializer.errors}, status=422, message="Validation error!")
    




class ProductRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductRetrieveSerializer

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return api_success(serializer.data, status=201, message="Product Details.")

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = ProductUpdateSerializer(instance, data=request.data, partial=partial)

        if serializer.is_valid():
            self.perform_update(serializer)
            return api_success(serializer.data, status=201, message="Product Update Successfully.")
        
        return api_error({'errors': serializer.errors}, status=422, message="Validation error!")
    






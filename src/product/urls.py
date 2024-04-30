from django.urls import path
from django.views.generic import TemplateView

from product.views.product import (
    CreateProductView, 
    ProductListView, 
    ProductCreateAPIView, 
    ProductRetrieveUpdateAPIView, 
    ProductVariantListAPIView, 
    UpdateProductView
)

from product.views.variant import VariantView, VariantCreateView, VariantEditView

app_name = "product"

urlpatterns = [
    # Variants URLs
    path('variants/', VariantView.as_view(), name='variants'),
    path('variant/create', VariantCreateView.as_view(), name='create.variant'),
    path('variant/<int:id>/edit', VariantEditView.as_view(), name='update.variant'),

    # Products URLs
    path('create/', CreateProductView.as_view(), name='create.product'),
    path('update/<int:pk>/', UpdateProductView.as_view(), name='update.product'),


    path('list/', ProductListView.as_view(), name='list.product'),



    ## Variants List API URLs
    path('variant-list/', ProductVariantListAPIView.as_view(), name='variant_list_api'),

    ## Create Products API 
    path('create-product/', ProductCreateAPIView.as_view(), name='create_product_api'),

    ## Retrieve and Update Products API 
    path('update-product/<int:pk>/', ProductRetrieveUpdateAPIView.as_view(), name='product_detail_api'),

]

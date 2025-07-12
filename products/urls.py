from django.urls import path, include
from .views import (
    ProductListCreateView,
    ProductDetailView,
    ProductImageUploadView,
)

urlpatterns = [
    path('', ProductListCreateView.as_view(), name='product-list-create'),
    path('<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('<int:product_id>/upload-image/', ProductImageUploadView.as_view(), name='product-image-upload'),
    path('<int:product_id>/reviews/', include('reviews.urls')),
]
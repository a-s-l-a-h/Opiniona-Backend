from rest_framework import generics, permissions, status
from rest_framework.exceptions import NotFound
from .models import Product
from .serializers import (
    ProductListSerializer,
    ProductDetailSerializer,
    ProductImageUploadSerializer
)
from .permissions import IsAdminOrReadOnly

class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all().order_by('name')
    serializer_class = ProductListSerializer
    permission_classes = [IsAdminOrReadOnly]

class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer
    permission_classes = [IsAdminOrReadOnly]

class ProductImageUploadView(generics.CreateAPIView):
    serializer_class = ProductImageUploadSerializer
    permission_classes = [permissions.IsAdminUser]

    def perform_create(self, serializer):
        product_id = self.kwargs.get('product_id')
        try:
            product = Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            raise NotFound("A product with this ID does not exist.")
        serializer.save(product=product)
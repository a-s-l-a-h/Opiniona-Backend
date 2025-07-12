from rest_framework import generics, permissions
from rest_framework.exceptions import ValidationError, NotFound
from .models import Review
from .serializers import ReviewSerializer
from products.models import Product

class ReviewListCreateView(generics.ListCreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        product_id = self.kwargs['product_id']
        return Review.objects.filter(product_id=product_id)

    def perform_create(self, serializer):
        product_id = self.kwargs.get('product_id')
        try:
            product = Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            raise NotFound("A product with this ID does not exist.")

        if Review.objects.filter(product=product, user=self.request.user).exists():
            raise ValidationError("You have already submitted a review for this product.")

        serializer.save(user=self.request.user, product=product)
from rest_framework import serializers
from .models import Product, ProductImage
from reviews.serializers import ReviewSerializer

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image']

class ProductImageUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['image']

class ProductListSerializer(serializers.ModelSerializer):
    average_rating = serializers.FloatField(read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    url = serializers.HyperlinkedIdentityField(view_name='product-detail', read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'url', 'name', 'price', 'average_rating', 'images']

class ProductDetailSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    average_rating = serializers.FloatField(read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'average_rating', 'images', 'reviews']
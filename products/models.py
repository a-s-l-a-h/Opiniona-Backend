from django.db import models
from django.db.models import Avg

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    @property
    def average_rating(self):
        return self.reviews.aggregate(avg_rating=Avg('rating'))['avg_rating'] or 0.0

def get_product_image_path(instance, filename):
    return f'products/{instance.product.id}/{filename}'

class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=get_product_image_path)

    def __str__(self):
        return f"Image for {self.product.name}"
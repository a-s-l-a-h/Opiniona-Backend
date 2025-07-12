
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from .models import Product, ProductImage

# This is the byte data for a tiny, valid 1x1 pixel GIF.
# We use this to satisfy the ImageField's validation that the uploaded file is a real image.
MINIMAL_GIF_BYTES = b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00\x00\x00\x00\xff\xff\xff\x21\xf9\x04\x01\x00\x00\x00\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x44\x01\x00\x3b'


class ProductTests(APITestCase):
    """
    Test suite for the Product model and its API endpoints.
    """

    def setUp(self):
        """
        Set up the necessary objects for the tests.
        """
        self.admin_user = User.objects.create_superuser(username='admin', password='password123', email='admin@example.com')
        self.regular_user = User.objects.create_user(username='user', password='password123', email='user@example.com')
        self.admin_token = Token.objects.create(user=self.admin_user)
        self.user_token = Token.objects.create(user=self.regular_user)
        self.product = Product.objects.create(name='Test Keyboard', description='A mechanical keyboard.', price='99.99')

    def test_list_products_unauthenticated(self):
        url = reverse('product-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_product_detail(self):
        url = reverse('product-detail', kwargs={'pk': self.product.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.product.name)

    def test_admin_can_create_product(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.admin_token.key)
        url = reverse('product-list-create')
        data = {'name': 'New Mouse', 'description': 'A new gaming mouse.', 'price': '59.99'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 2)
        self.assertEqual(Product.objects.latest('id').name, 'New Mouse')

    def test_regular_user_cannot_create_product(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_token.key)
        url = reverse('product-list-create')
        data = {'name': 'Unauthorized Product', 'description': 'This should not be created.', 'price': '10.00'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_update_product(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.admin_token.key)
        url = reverse('product-detail', kwargs={'pk': self.product.pk})
        updated_data = {'name': 'Updated Keyboard', 'description': 'An updated description.', 'price': '109.99'}
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.product.refresh_from_db()
        self.assertEqual(self.product.name, 'Updated Keyboard')

    def test_regular_user_cannot_update_product(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_token.key)
        url = reverse('product-detail', kwargs={'pk': self.product.pk})
        updated_data = {'name': 'Unauthorized Update'}
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_delete_product(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.admin_token.key)
        url = reverse('product-detail', kwargs={'pk': self.product.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Product.objects.count(), 0)

    # --- Image Upload Tests ---
    
    def test_admin_can_upload_image_for_product(self):
        """
        Ensure an admin can upload an image for a product.
        """
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.admin_token.key)
        url = reverse('product-image-upload', kwargs={'product_id': self.product.pk})
        
        # <<< CORRECTED LINE: Use the valid GIF bytes instead of simple text bytes.
        image = SimpleUploadedFile("test_image.gif", MINIMAL_GIF_BYTES, content_type="image/gif")
        data = {'image': image}
        
        response = self.client.post(url, data, format='multipart')
        
        # Now this assertion should pass!
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ProductImage.objects.count(), 1)
        self.assertEqual(ProductImage.objects.first().product, self.product)
        
    def test_regular_user_cannot_upload_image(self):
        """
        Ensure a regular user cannot upload an image.
        """
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_token.key)
        url = reverse('product-image-upload', kwargs={'product_id': self.product.pk})
        
        image = SimpleUploadedFile("test_image.gif", MINIMAL_GIF_BYTES, content_type="image/gif")
        data = {'image': image}
        response = self.client.post(url, data, format='multipart')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
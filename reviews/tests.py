# reviews/tests.py

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from products.models import Product
from .models import Review

class ReviewTests(APITestCase):
    """
    Test suite for the Review model and its API endpoints.
    """

    def setUp(self):
        """
        Set up initial objects for testing reviews.
        """
        self.regular_user = User.objects.create_user(username='user', password='password123')
        self.another_user = User.objects.create_user(username='anotheruser', password='password123')
        self.user_token = Token.objects.create(user=self.regular_user)
        
        self.product = Product.objects.create(name='Test Monitor', description='A 4K Monitor.', price='299.99')

    # --- Review Creation Tests ---

    def test_authenticated_user_can_create_review(self):
        """
        Ensure a logged-in user can successfully post a review.
        """
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_token.key)
        url = reverse('review-list-create', kwargs={'product_id': self.product.pk})
        data = {'rating': 5, 'feedback': 'This is an amazing monitor!'}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Review.objects.count(), 1)
        self.assertEqual(Review.objects.first().user, self.regular_user)
        self.assertEqual(Review.objects.first().product, self.product)

    def test_unauthenticated_user_cannot_create_review(self):
        """
        Ensure an anonymous user cannot post a review.
        """
        url = reverse('review-list-create', kwargs={'product_id': self.product.pk})
        data = {'rating': 5, 'feedback': 'This should not work.'}
        response = self.client.post(url, data, format='json')

        # <<< CORRECTED LINE: Changed to 401 Unauthorized, which is the correct response for a missing token.
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED) 

    def test_cannot_create_duplicate_review(self):
        """
        Ensure a user cannot review the same product twice.
        """
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_token.key)
        url = reverse('review-list-create', kwargs={'product_id': self.product.pk})
        data = {'rating': 4, 'feedback': 'First review.'}

        # First review should succeed
        first_response = self.client.post(url, data, format='json')
        self.assertEqual(first_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Review.objects.count(), 1)
        
        # Second review for the same product by the same user should fail
        second_response = self.client.post(url, {'rating': 2, 'feedback': 'Duplicate review.'}, format='json')
        self.assertEqual(second_response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Review.objects.count(), 1)

    def test_invalid_rating_is_rejected(self):
        """
        Ensure a review with an invalid rating (e.g., 0 or 6) is rejected.
        """
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_token.key)
        url = reverse('review-list-create', kwargs={'product_id': self.product.pk})
        
        invalid_data_low = {'rating': 0, 'feedback': 'Rating too low.'}
        response_low = self.client.post(url, invalid_data_low, format='json')
        self.assertEqual(response_low.status_code, status.HTTP_400_BAD_REQUEST)
        
        invalid_data_high = {'rating': 6, 'feedback': 'Rating too high.'}
        response_high = self.client.post(url, invalid_data_high, format='json')
        self.assertEqual(response_high.status_code, status.HTTP_400_BAD_REQUEST)

    # --- Data Aggregation Test ---
    
    def test_product_average_rating_updates_correctly(self):
        """
        Ensure the product's average_rating property is calculated correctly after new reviews.
        """
        self.product.refresh_from_db()
        self.assertEqual(self.product.average_rating, 0.0)

        # First review by regular_user (rating: 5)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_token.key)
        review_url = reverse('review-list-create', kwargs={'product_id': self.product.pk})
        self.client.post(review_url, {'rating': 5, 'feedback': 'Excellent!'}, format='json')
        
        self.product.refresh_from_db()
        self.assertEqual(self.product.average_rating, 5.0)

        # Second review by another_user (rating: 3)
        another_user_token = Token.objects.create(user=self.another_user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + another_user_token.key)
        self.client.post(review_url, {'rating': 3, 'feedback': 'It was okay.'}, format='json')
        
        self.assertEqual(self.product.reviews.count(), 2)
        self.product.refresh_from_db()
        self.assertEqual(self.product.average_rating, 4.0)
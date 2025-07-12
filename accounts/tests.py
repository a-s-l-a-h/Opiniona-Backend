# accounts/tests.py

from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.authtoken.models import Token


class UserRegistrationTestCase(APITestCase):
    """Test cases for user registration"""
    
    def setUp(self):
        self.register_url = reverse('register')
        self.valid_user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpass123',
            'password2': 'testpass123',
            'first_name': 'Test',
            'last_name': 'User'
        }
    
    def test_user_registration_success(self):
        """Test successful user registration"""
        response = self.client.post(self.register_url, self.valid_user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username='testuser').exists())
        
        # Check if user data is saved correctly
        user = User.objects.get(username='testuser')
        self.assertEqual(user.email, 'test@example.com')
        self.assertEqual(user.first_name, 'Test')
        self.assertEqual(user.last_name, 'User')
    
    def test_user_registration_password_mismatch(self):
        """Test registration with mismatched passwords"""
        data = self.valid_user_data.copy()
        data['password2'] = 'differentpass123'
        
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', response.data)
        self.assertFalse(User.objects.filter(username='testuser').exists())
    
    def test_user_registration_duplicate_username(self):
        """Test registration with duplicate username"""
        # Create a user first
        User.objects.create_user(username='testuser', email='existing@example.com')
        
        response = self.client.post(self.register_url, self.valid_user_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('username', response.data)
    
    def test_user_registration_duplicate_email(self):
        """Test registration with duplicate email"""
        # Create a user first
        User.objects.create_user(username='existinguser', email='test@example.com')
        
        response = self.client.post(self.register_url, self.valid_user_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)
    
    def test_user_registration_missing_fields(self):
        """Test registration with missing required fields"""
        response = self.client.post(self.register_url, {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('username', response.data)
        self.assertIn('email', response.data)
        self.assertIn('password', response.data)
    
    def test_user_registration_short_password(self):
        """Test registration with password too short"""
        data = self.valid_user_data.copy()
        data['password'] = '123'
        data['password2'] = '123'
        
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', response.data)
    
    def test_user_registration_invalid_email(self):
        """Test registration with invalid email"""
        data = self.valid_user_data.copy()
        data['email'] = 'invalid-email'
        
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)


class UserLoginTestCase(APITestCase):
    """Test cases for user login"""
    
    def setUp(self):
        self.login_url = reverse('login')
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_user_login_success(self):
        """Test successful user login"""
        data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
        self.assertIn('user_id', response.data)
        self.assertIn('is_staff', response.data)
        self.assertEqual(response.data['user_id'], self.user.pk)
        self.assertFalse(response.data['is_staff'])
    
    def test_user_login_invalid_credentials(self):
        """Test login with invalid credentials"""
        data = {
            'username': 'testuser',
            'password': 'wrongpassword'
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('non_field_errors', response.data)
    
    def test_user_login_missing_username(self):
        """Test login with missing username"""
        data = {
            'password': 'testpass123'
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('username', response.data)
    
    def test_user_login_missing_password(self):
        """Test login with missing password"""
        data = {
            'username': 'testuser'
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', response.data)
    
    def test_user_login_nonexistent_user(self):
        """Test login with non-existent user"""
        data = {
            'username': 'nonexistent',
            'password': 'testpass123'
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_admin_user_login(self):
        """Test login with admin user"""
        admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpass123'
        )
        
        data = {
            'username': 'admin',
            'password': 'adminpass123'
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['is_staff'])
    
    def test_token_creation_on_login(self):
        """Test that token is created on login"""
        data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check if token exists in database
        token = Token.objects.get(user=self.user)
        self.assertEqual(token.key, response.data['token'])


class UserLogoutTestCase(APITestCase):
    """Test cases for user logout"""
    
    def setUp(self):
        self.logout_url = reverse('logout')
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.token = Token.objects.create(user=self.user)
    
    def test_user_logout_success(self):
        """Test successful user logout"""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.post(self.logout_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['detail'], 'Successfully logged out.')
        
        # Check if token is deleted
        self.assertFalse(Token.objects.filter(key=self.token.key).exists())
    
    def test_user_logout_without_authentication(self):
        """Test logout without authentication"""
        response = self.client.post(self.logout_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('detail', response.data)
    
    def test_user_logout_with_invalid_token(self):
        """Test logout with invalid token"""
        self.client.credentials(HTTP_AUTHORIZATION='Token invalid_token')
        response = self.client.post(self.logout_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_user_logout_get_method_not_allowed(self):
        """Test that GET method is not allowed for logout"""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.get(self.logout_url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
    
    def test_user_logout_multiple_times(self):
        """Test logout multiple times (should handle gracefully)"""
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        
        # First logout
        response1 = self.client.post(self.logout_url)
        self.assertEqual(response1.status_code, status.HTTP_200_OK)
        
        # Second logout attempt (token should be deleted)
        response2 = self.client.post(self.logout_url)
        self.assertEqual(response2.status_code, status.HTTP_401_UNAUTHORIZED)


class UserModelTestCase(TestCase):
    """Test cases for User model interactions"""
    
    def test_user_creation(self):
        """Test user creation"""
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'test@example.com')
        self.assertTrue(user.check_password('testpass123'))
    
    def test_superuser_creation(self):
        """Test superuser creation"""
        admin = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpass123'
        )
        self.assertTrue(admin.is_staff)
        self.assertTrue(admin.is_superuser)
    
    def test_user_string_representation(self):
        """Test user string representation"""
        user = User.objects.create_user(username='testuser')
        self.assertEqual(str(user), 'testuser')


class TokenTestCase(APITestCase):
    """Test cases for Token functionality"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_token_creation_on_user_creation(self):
        """Test that token can be created for user"""
        token = Token.objects.create(user=self.user)
        self.assertEqual(token.user, self.user)
        self.assertTrue(len(token.key) > 0)
    
    def test_token_uniqueness(self):
        """Test that each user has a unique token"""
        user2 = User.objects.create_user(
            username='testuser2',
            email='test2@example.com',
            password='testpass123'
        )
        
        token1 = Token.objects.create(user=self.user)
        token2 = Token.objects.create(user=user2)
        
        self.assertNotEqual(token1.key, token2.key)


class IntegrationTestCase(APITestCase):
    """Integration tests for complete user flow"""
    
    def test_complete_user_flow(self):
        """Test complete user registration -> login -> logout flow"""
        # 1. Register user
        register_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpass123',
            'password2': 'testpass123'
        }
        register_response = self.client.post(reverse('register'), register_data)
        self.assertEqual(register_response.status_code, status.HTTP_201_CREATED)
        
        # 2. Login user
        login_data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        login_response = self.client.post(reverse('login'), login_data)
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)
        token = login_response.data['token']
        
        # 3. Logout user
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        logout_response = self.client.post(reverse('logout'))
        self.assertEqual(logout_response.status_code, status.HTTP_200_OK)
        
        # 4. Try to logout again (should fail)
        logout_response2 = self.client.post(reverse('logout'))
        self.assertEqual(logout_response2.status_code, status.HTTP_401_UNAUTHORIZED)
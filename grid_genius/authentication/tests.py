from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .forms import SignUpForm, LoginForm

class UserAuthTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.signup_url = reverse('authentication:signup')
        self.login_url = reverse('authentication:login')
        self.home_url = reverse('authentication:home')
        self.logout_url = reverse('authentication:logout')
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='password123')

    def test_home_view_requires_login(self):
        """Test that the home view requires the user to be logged in."""
        response = self.client.get(self.home_url)
        self.assertEqual(response.status_code, 302)  # Redirect to login

    def test_signup_view_get(self):
        """Test that the signup view renders properly with a GET request."""
        response = self.client.get(self.signup_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/signup.html')

    def test_signup_view_post_valid(self):
        """Test that a valid POST request to signup view creates a user."""
        response = self.client.post(self.signup_url, {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'password123',
            'password2': 'password123'
        })
        self.assertEqual(response.status_code, 302)  # Redirect to login
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_signup_view_post_invalid_email(self):
        """Test that the signup view handles duplicate email correctly."""
        response = self.client.post(self.signup_url, {
            'username': 'anotheruser',
            'email': 'test@example.com',  # Same email as existing user
            'password1': 'password123',
            'password2': 'password123'
        })
        self.assertEqual(response.status_code, 302)
        self.assertFalse(User.objects.filter(username='anotheruser').exists())

    def test_login_view_get(self):
        """Test that the login view renders properly with a GET request."""
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/login.html')

    def test_login_view_post_valid(self):
        """Test that a valid POST request to login view logs in the user."""
        response = self.client.post(self.login_url, {
            'username': 'testuser',
            'password': 'password123'
        })
        self.assertEqual(response.status_code, 302)  # Redirect to home

    def test_login_view_post_invalid(self):
        """Test that an invalid POST request to login view returns an error."""
        response = self.client.post(self.login_url, {
            'username': 'wronguser',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)  # Re-render login
        self.assertContains(response, 'Invalid username or password.')

    def test_logout_view(self):
        """Test that the logout view logs the user out and redirects to login."""
        self.client.login(username='testuser', password='password123')
        response = self.client.get(self.logout_url)
        self.assertEqual(response.status_code, 302)  # Redirect to login
        response = self.client.get(self.home_url)
        self.assertEqual(response.status_code, 302)  # Redirect to login after logout

    def test_about_view(self):
        """Test that the about view renders correctly."""
        url = reverse('about')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'about.html')

    def test_contact_view(self):
        """Test that the contact view renders correctly."""
        url = reverse('contact')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'contact.html')

    def test_service_view(self):
        """Test that the service view renders correctly."""
        url = reverse('service')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'service.html')

    def test_portfolio_view(self):
        """Test that the portfolio view renders correctly."""
        url = reverse('portfolio')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'portfolio.html')
        



    def test_home_view_logged_in(self):
        """Test that the home view is accessible to logged-in users."""
        self.client.login(username='testuser', password='password123')
        response = self.client.get(self.home_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    def test_home_view_redirects_if_not_logged_in(self):
        """Test that the home view redirects if the user is not logged in."""
        response = self.client.get(self.home_url)
        self.assertEqual(response.status_code, 302)  # Should redirect to login

    def test_about_view(self):
        """Test that the about view renders correctly."""
        url = reverse('about')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'about.html')

    def test_contact_view(self):
        """Test that the contact view renders correctly."""
        url = reverse('contact')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'contact.html')

    def test_service_view(self):
        """Test that the service view renders correctly."""
        url = reverse('service')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'service.html')

    def test_portfolio_view(self):
        """Test that the portfolio view renders correctly."""
        url = reverse('portfolio')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'portfolio.html')

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import User

class APITestCase(TestCase):
    def setUp(self):
        """
        Set up the test environment. Initialize the API client and define test user data.
        """
        self.client = APIClient()
        self.user_data = {
            "aadhar_id": "123456789012",
            "full_name": "John Doe",  # Updated key to match the model field
            "email": "john.doe@example.com",
            "annual_income": 500000.00,  # Ensure data matches the model field type
        }

    def test_register_user(self):
        """
        Test the user registration API endpoint.
        Ensure that a new user can be successfully registered.
        """
        response = self.client.post(reverse('register-user'), self.user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)  # Verify user is created in the database
        self.assertEqual(User.objects.first().email, self.user_data["email"])  # Verify saved data matches input

    def test_apply_loan(self):
        """
        Test the loan application API endpoint.
        Ensure that a loan can be applied for an existing user.
        """
        user = User.objects.create(**self.user_data)  # Create a test user
        loan_data = {
            "user": user.id,
            "loan_amount": 1000.00,
            "interest_rate": 12.00,
            "term_period_months": 12,  # Updated to match the model's field name
            "disbursement_date": "2024-01-01"
        }
        response = self.client.post(reverse('apply-loan'), loan_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Optionally, add assertions to check if the loan was properly created

from django.db import models
from uuid import uuid4

class User(models.Model):
    aadhar_id = models.CharField(max_length=12, unique=True)
    full_name = models.CharField(max_length=100)  # Changed `name` to `full_name` for clarity
    email = models.EmailField(unique=True)
    annual_income = models.DecimalField(max_digits=12, decimal_places=2)  # Increased max_digits for better range
    credit_score = models.PositiveIntegerField(default=300)  # Changed to PositiveIntegerField for validation

    def __str__(self):
        return self.full_name

class Loan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    loan_type = models.CharField(max_length=100, default="Credit Card Loan")  # Increased max_length for more flexibility
    loan_amount = models.DecimalField(max_digits=12, decimal_places=2)  # Increased max_digits for better range
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    term_period_months = models.PositiveIntegerField()  # Renamed `term_period` for better readability
    disbursement_date = models.DateField()
    loan_id = models.UUIDField(default=uuid4, unique=True, editable=False)  # Made `loan_id` non-editable

class Billing(models.Model):
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE)
    billing_date = models.DateField()
    due_date = models.DateField()
    principal_due = models.DecimalField(max_digits=12, decimal_places=2)  # Increased max_digits for better range
    interest_due = models.DecimalField(max_digits=12, decimal_places=2)  # Increased max_digits for better range
    total_due = models.DecimalField(max_digits=12, decimal_places=2)  # Increased max_digits for better range
    is_paid = models.BooleanField(default=False)

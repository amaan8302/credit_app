from rest_framework import serializers
from .models import User, Loan, Billing

class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source='full_name', required=True)  # Explicitly serialized

    class Meta:
        model = User
        fields = ['id', 'aadhar_id', 'full_name', 'email', 'annual_income', 'credit_score']  # Explicitly listing fields

class LoanSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())  # Serialize user as a reference

    class Meta:
        model = Loan
        fields = [
            'id', 'user', 'loan_type', 'loan_amount', 
            'interest_rate', 'term_period_months', 
            'disbursement_date', 'loan_id'
        ]  # Explicitly listed fields for clarity

class BillingSerializer(serializers.ModelSerializer):
    loan = serializers.PrimaryKeyRelatedField(queryset=Loan.objects.all())  # Serialize loan as a reference

    class Meta:
        model = Billing
        fields = [
            'id', 'loan', 'billing_date', 'due_date', 
            'principal_due', 'interest_due', 'total_due', 
            'is_paid'
        ]  # Explicitly listed fields for clarity

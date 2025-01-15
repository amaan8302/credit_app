from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User, Loan, Billing
from .serializers import UserSerializer, LoanSerializer
from .tasks import calculate_credit_score
from django.utils.timezone import now

class RegisterUser(APIView):
    """
    API endpoint to register a new user.
    Triggers a Celery task to calculate the user's credit score upon successful registration.
    """
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            calculate_credit_score.delay(user.id)  # Trigger asynchronous credit score calculation
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ApplyLoan(APIView):
    """
    API endpoint to apply for a loan.
    Checks user's credit score and annual income before approving the loan.
    """
    def post(self, request):
        serializer = LoanSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user = User.objects.get(id=request.data['user'])
                # Validate loan eligibility criteria
                if user.credit_score >= 450 and user.annual_income >= 150000:
                    loan = serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                return Response({"error": "Loan criteria not met"}, status=status.HTTP_400_BAD_REQUEST)
            except User.DoesNotExist:
                return Response({"error": "User not found"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MakePayment(APIView):
    """
    API endpoint to make a payment for a loan.
    Ensures the payment covers the total due amount and updates the billing record.
    """
    def post(self, request):
        loan_id = request.data.get('loan_id')
        amount = request.data.get('amount')
        try:
            loan = Loan.objects.get(loan_id=loan_id)
            billing = Billing.objects.filter(loan=loan, is_paid=False).first()
            if not billing:
                return Response({"error": "No pending dues"}, status=status.HTTP_400_BAD_REQUEST)
            if amount < billing.total_due:
                return Response({"error": "Payment is less than the due amount"}, status=status.HTTP_400_BAD_REQUEST)
            # Mark the billing as paid
            billing.is_paid = True
            billing.save()
            return Response({"message": "Payment successful"}, status=status.HTTP_200_OK)
        except Loan.DoesNotExist:
            return Response({"error": "Loan not found"}, status=status.HTTP_400_BAD_REQUEST)

class GetStatement(APIView):
    """
    API endpoint to fetch the loan statement, including past and upcoming transactions.
    """
    def get(self, request):
        loan_id = request.query_params.get('loan_id')
        try:
            loan = Loan.objects.get(loan_id=loan_id)
            # Fetch past and upcoming transactions
            past_transactions = Billing.objects.filter(loan=loan, billing_date__lt=now().date())
            upcoming_transactions = Billing.objects.filter(loan=loan, billing_date__gte=now().date())
            return Response({
                "past_transactions": [
                    {
                        "date": transaction.billing_date,
                        "principal_due": transaction.principal_due,
                        "interest_due": transaction.interest_due,
                        "total_due": transaction.total_due,
                        "is_paid": transaction.is_paid
                    } for transaction in past_transactions
                ],
                "upcoming_transactions": [
                    {
                        "date": transaction.billing_date,
                        "principal_due": transaction.principal_due,
                        "interest_due": transaction.interest_due,
                        "total_due": transaction.total_due
                    } for transaction in upcoming_transactions
                ]
            }, status=status.HTTP_200_OK)
        except Loan.DoesNotExist:
            return Response({"error": "Loan not found"}, status=status.HTTP_400_BAD_REQUEST)

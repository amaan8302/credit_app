from celery import shared_task
from datetime import timedelta
from django.utils.timezone import now
from .models import User, Billing, Loan

@shared_task
def calculate_credit_score(user_id):
    """
    Task to calculate and update the credit score for a specific user.
    The logic here can be replaced with an actual credit score calculation algorithm.
    """
    try:
        user = User.objects.get(id=user_id)
        # Example logic for credit score calculation (replace with real logic as needed)
        user.credit_score = 700  # Placeholder score for demonstration
        user.save()
    except User.DoesNotExist:
        # Handle case where the user does not exist
        pass

@shared_task
def generate_billing():
    """
    Task to generate billing entries for loans that require a new bill on the current date.
    Calculates principal and interest dues and creates a billing record for each eligible loan.
    """
    loans = Loan.objects.all()
    today = now().date()

    for loan in loans:
        # Calculate the next billing date (30 days after disbursement)
        billing_date = loan.disbursement_date + timedelta(days=30)
        
        if today == billing_date:  # Generate billing only if today's date matches
            # Calculate interest and principal dues
            interest_due = (loan.loan_amount * loan.interest_rate / 100) / 12
            principal_due = loan.loan_amount / loan.term_period_months
            total_due = principal_due + interest_due

            # Create a billing record
            Billing.objects.create(
                loan=loan,
                billing_date=billing_date,
                due_date=billing_date + timedelta(days=15),  # Due date is 15 days after billing
                principal_due=principal_due,
                interest_due=interest_due,
                total_due=total_due,
            )

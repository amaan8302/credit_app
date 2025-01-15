from django.urls import path
from .views import RegisterUser, ApplyLoan, MakePayment, GetStatement

# URL patterns for the API endpoints
urlpatterns = [
    # Endpoint for registering a new user
    path('api/register-user/', RegisterUser.as_view(), name='register-user'),

    # Endpoint for applying for a loan
    path('api/apply-loan/', ApplyLoan.as_view(), name='apply-loan'),

    # Endpoint for making loan payments
    path('api/make-payment/', MakePayment.as_view(), name='make-payment'),

    # Endpoint for retrieving loan statements
    path('api/get-statement/', GetStatement.as_view(), name='get-statement'),
]

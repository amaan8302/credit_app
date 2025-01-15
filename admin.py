from django.contrib import admin
from .models import User, Loan, Billing

admin.site.register(User)
admin.site.register(Loan)
admin.site.register(Billing)
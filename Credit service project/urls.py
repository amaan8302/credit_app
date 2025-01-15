from django.contrib import admin
from django.urls import path, include

# URL routing for the project
urlpatterns = [
    # Admin panel URL
    path('admin/', admin.site.urls),

    # Include URLs from the credit_service_app
    path('', include('credit_service_app.urls')),
]
